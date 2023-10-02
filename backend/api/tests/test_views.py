from unittest.mock import patch

import pyotp
from codeforlife.tests import CronTestCase
from codeforlife.user.models import AuthFactor, User
from django.core import management
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.get(id=2)

    def test_post__otp(self):
        AuthFactor.objects.create(
            user=self.user,
            type=AuthFactor.Type.OTP,
        )

        response = self.client.post(
            reverse("login", kwargs={"form": "email"}),
            data={
                "email": self.user.email,
                "password": "Password1",
            },
        )

        assert response.status_code == 200
        self.assertDictEqual(
            response.json(),
            {
                "auth_factors": [AuthFactor.Type.OTP],
                "otp_bypass_token_exists": False,
            },
        )

        self.user.userprofile.otp_secret = pyotp.random_base32()
        self.user.userprofile.save()

        totp = pyotp.TOTP(self.user.userprofile.otp_secret)

        now = timezone.now()
        with patch.object(timezone, "now", return_value=now):
            response = self.client.post(
                reverse("login", kwargs={"form": "otp"}),
                data={"otp": totp.at(now)},
            )

        assert response.status_code == 200
        self.assertDictEqual(
            response.json(),
            {
                "auth_factors": [],
                "otp_bypass_token_exists": False,
            },
        )


class TestClearExpiredView(CronTestCase):
    def test_clear_expired_view(self):
        with patch.object(management, "call_command") as call_command:
            self.client.get(reverse("clear-expired-sessions"))
            call_command.assert_called_once_with("clearsessions")
