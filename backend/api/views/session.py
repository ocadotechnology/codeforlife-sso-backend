import logging

# from codeforlife.user.models import User
from codeforlife.mixins import CronMixin
from common.models import UserSession
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.sessions.models import Session, SessionManager
from django.core.management import call_command
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from ..forms import (
    BaseAuthForm,
    EmailAuthForm,
    OtpAuthForm,
    UserIdAuthForm,
    UsernameAuthForm,
)


# TODO: add 2FA logic
class LoginView(_LoginView):
    def get_form_class(self):
        if "email" in self.request.POST:
            return EmailAuthForm
        elif "username" in self.request.POST:
            return UsernameAuthForm
        elif "user_id" in self.request.POST:
            return UserIdAuthForm
        elif "otp" in self.request.POST:  # TODO: add 2fa logic.
            return OtpAuthForm
        raise Exception()  # TODO: handle this

    def form_valid(self, form: BaseAuthForm):
        login(self.request, form.user)

        # TODO: use google analytics
        user_session = {"user": form.user}
        if self.get_form_class() in [UsernameAuthForm, UserIdAuthForm]:
            user_session["class_field"] = form.user.new_student.class_field
            user_session["login_type"] = (
                "direct" if "user_id" in self.request.POST else "classform"
            )
        UserSession.objects.create(**user_session)

        return HttpResponse()


class ClearExpiredView(CronMixin, APIView):
    def get(self, request):
        # objects is missing type SessionManager
        session_objects: SessionManager = Session.objects

        before_session_count = session_objects.all().count()
        logging.info(f"Session count before clearance: {before_session_count}")

        # Clears expired sessions.
        # https://docs.djangoproject.com/en/3.2/ref/django-admin/#clearsessions
        call_command("clearsessions")

        after_session_count = session_objects.all().count()
        logging.info(f"Session count after clearance: {after_session_count}")
        session_clearance_count = before_session_count - after_session_count
        logging.info(f"Session clearance count: {session_clearance_count}")

        return Response()
