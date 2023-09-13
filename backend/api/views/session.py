import typing as t

from common.models import UserSession
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as _LoginView
from django.http import HttpResponse

from ..forms import (
    CredentialsForm,
    DependentStudentAuthForm,
    OneTimePasswordForm,
)


# TODO: add 2FA logic
class LoginView(_LoginView):
    def get_form_class(self):
        user_type: str = self.kwargs["user_type"]
        if user_type == "independent_student":
            return CredentialsForm
        elif user_type == "dependent_student":
            return DependentStudentAuthForm
        else:
            return CredentialsForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        user = form.get_user()

        # teacher
        if user.new_teacher is not None:
            pass

        UserSession.objects.create(user=user)

        return super().form_valid(form)
