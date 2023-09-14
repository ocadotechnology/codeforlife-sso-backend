import typing as t

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UsernameField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.http import HttpRequest


class BaseAuthForm(forms.Form):
    def __init__(self, request: HttpRequest, *args, **kwargs):
        self.request = request
        self.user: t.Optional[AbstractBaseUser] = None

    def clean(self, **kwargs):
        self.user = authenticate(self.request, **kwargs)
        if self.user is None:
            raise ValidationError(
                self.get_invalid_login_error_message(),
                code="invalid_login",
            )
        # TODO: confirm if we should return error message if is_active=False

        return self.cleaned_data

    # Required by Django's LoginView
    def get_user(self):
        return self.user

    def get_invalid_login_error_message(self) -> str:
        raise NotImplementedError()


class CredentialsForm(BaseAuthForm):
    email = forms.EmailField()
    # TODO: use regex validator
    password = forms.CharField(strip=False)

    def clean(self):
        return super().clean(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

    def get_invalid_login_error_message(self):
        return (
            "Please enter a correct username and password. Note that both"
            " fields may be case-sensitive."
        )


class OneTimePasswordForm(BaseAuthForm):
    otp = forms.CharField(
        validators=[
            RegexValidator(r"^[0-9]{6}$", "Must be 6 digits"),
        ],
    )

    def clean(self):
        # TODO: implement 2FA flow
        return super().clean(
            otp=self.cleaned_data["otp"],
        )


class DependentStudentUsernameCredentialsForm(BaseAuthForm):
    username = UsernameField()
    # TODO: use regex validator
    password = forms.CharField(strip=False)
    class_id = forms.CharField(
        validators=[
            RegexValidator(
                r"^[A-Z]{2}[0-9]{3}$",
                "Must be 2 upper case letters followed by 3 digits",
            ),
        ],
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            return super().clean(
                username=username,
                password=password,
                class_id=self.cleaned_data["class_id"],
            )

        return self.cleaned_data


class DependentStudentUserIdCredentialsForm(BaseAuthForm):
    user_id = forms.IntegerField(min_value=1)
    login_id = forms.CharField(min_length=32, max_length=32)

    def clean(self):
        return super().clean(
            userId=self.cleaned_data["user_id"],
            login_id=self.cleaned_data["login_id"],
        )
