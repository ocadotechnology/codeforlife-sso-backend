import json
import logging

from codeforlife.mixins import CronMixin
from codeforlife.request import HttpRequest, Request
from codeforlife.user.models import AuthFactor, User
from common.models import UserSession
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.sessions.models import Session, SessionManager
from django.core import management
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
    BaseAuthForm,
    EmailAuthForm,
    OtpAuthForm,
    OtpBypassTokenAuthForm,
    UserIdAuthForm,
    UsernameAuthForm,
)
from .permissions import UserHasSessionAuthFactors


class LoginView(_LoginView):
    request: HttpRequest

    def get_form_class(self):
        form = self.kwargs["form"]
        if form == "email":
            return EmailAuthForm
        elif form == "username":
            return UsernameAuthForm
        elif form == "user-id":
            return UserIdAuthForm
        elif form == "otp":
            return OtpAuthForm
        elif form == "otp-bypass-token":
            return OtpBypassTokenAuthForm

    def form_valid(self, form: BaseAuthForm):
        # Clear expired sessions.
        self.request.session.clear_expired(form.user.id)

        # Create session (without data).
        login(self.request, form.user)
        user = self.request.user

        # TODO: use google analytics
        user_session = {"user": form.user}
        if self.get_form_class() in [UsernameAuthForm, UserIdAuthForm]:
            user_session["class_field"] = form.user.new_student.class_field
            user_session["login_type"] = (
                "direct" if "user_id" in self.request.POST else "classform"
            )
        UserSession.objects.create(**user_session)

        # Save session (with data).
        self.request.session.save()

        # Create a non-HTTP-only session cookie with the pending auth factors.
        response = HttpResponse()
        response.set_cookie(
            key="sessionid_httponly_false",
            value=json.dumps(
                {
                    "user_id": user.id,
                    "auth_factors": list(
                        user.session.session_auth_factors.values_list(
                            "auth_factor__type", flat=True
                        )
                    ),
                },
                separators=(",", ":"),
                indent=None,
            ),
            max_age=(
                None
                if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE
                else settings.SESSION_COOKIE_AGE
            ),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            domain=settings.SESSION_COOKIE_DOMAIN,
            httponly=False,
        )

        return response

    def form_invalid(self, form: BaseAuthForm):
        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginOptionsView(APIView):
    http_method_names = ["get"]
    permission_classes = [UserHasSessionAuthFactors]

    def get(self, request: Request):
        user: User = request.user
        session_auth_factors = user.session.session_auth_factors

        response_data = {"id": user.id}
        if session_auth_factors.filter(
            auth_factor__type=AuthFactor.Type.OTP
        ).exists():
            response_data[
                "otp_bypass_token_exists"
            ] = user.otp_bypass_tokens.exists()

        return Response(response_data)


class ClearExpiredView(CronMixin, APIView):
    def get(self, request):
        # objects is missing type SessionManager
        session_objects: SessionManager = Session.objects

        before_session_count = session_objects.count()
        logging.info(f"Session count before clearance: {before_session_count}")

        # Clears expired sessions.
        # https://docs.djangoproject.com/en/3.2/ref/django-admin/#clearsessions
        management.call_command("clearsessions")

        after_session_count = session_objects.count()
        logging.info(f"Session count after clearance: {after_session_count}")
        session_clearance_count = before_session_count - after_session_count
        logging.info(f"Session clearance count: {session_clearance_count}")

        return Response()
