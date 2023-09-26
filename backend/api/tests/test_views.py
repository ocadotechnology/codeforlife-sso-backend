from unittest.mock import Mock, patch

from codeforlife.tests import CronTestCase
from django.urls import reverse


class TestClearExpiredView(CronTestCase):
    @patch("django.core.management.call_command")
    def test_clear_expired_view(self, call_command: Mock):
        self.client.get(reverse("clear-expired-sessions"))

        call_command.assert_called_once_with("clearsessions")
