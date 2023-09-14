import typing as t
from enum import Enum
from functools import cached_property

from common.models import UserSession
from django.contrib.auth.views import LoginView as _LoginView

from ..forms import (
    BaseAuthForm,
    CredentialsForm,
    DependentStudentUserIdCredentialsForm,
    DependentStudentUsernameCredentialsForm,
    OneTimePasswordForm,
)


# TODO: move to codeforlife package
class UserType(str, Enum):
    TEACHER = "teacher"
    DEP_STUDENT = "dependent_student"
    INDEP_STUDENT = "independent_student"


# TODO: add 2FA logic
class LoginView(_LoginView):
    @cached_property
    def user_type(self) -> UserType:
        return UserType(self.kwargs["user_type"])

    def get_form_class(self):
        if self.user_type == UserType.INDEP_STUDENT:
            return CredentialsForm

        elif self.user_type == UserType.DEP_STUDENT:
            if "user_id" in self.request.POST:
                return DependentStudentUserIdCredentialsForm
            return DependentStudentUsernameCredentialsForm

        else:  # user_type == UserType.TEACHER
            if False:  # TODO: add 2fa logic.
                return OneTimePasswordForm
            return CredentialsForm

    def form_valid(self, form: BaseAuthForm):
        response = super().form_valid(form)

        # TODO: use google analytics
        user = form.get_user()
        user_session = {"user": user}
        if self.user_type == UserType.DEP_STUDENT:
            user_session["class_field"] = user.new_student.class_field
            user_session["login_type"] = (
                "direct" if "user_id" in self.request.POST else "classform"
            )
        UserSession.objects.create(**user_session)

        return response
