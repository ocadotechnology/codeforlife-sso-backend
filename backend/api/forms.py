from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.core.validators import RegexValidator


class BaseAuthForm(forms.Form):
    def __init__(self, request: WSGIRequest, *args, **kwargs):
        self.request = request
        self.user: AbstractBaseUser = None
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.errors:
            raise ValidationError(
                "Found form errors. Skipping authentication.",
                code="form_errors",
            )

        self.user = authenticate(
            self.request,
            **{key: self.cleaned_data[key] for key in self.fields.keys()}
        )
        if self.user is None:
            raise ValidationError(
                self.get_invalid_login_error_message(),
                code="invalid_login",
            )
        elif not self.user.is_active:
            raise ValidationError(
                "User is not active",
                code="user_not_active",
            )

        return self.cleaned_data

    def get_invalid_login_error_message(self) -> str:
        raise NotImplementedError()


class OtpAuthForm(BaseAuthForm):
    otp = forms.CharField(
        validators=[
            RegexValidator(r"^[0-9]{6}$", "Must be 6 digits"),
        ],
    )

    def get_invalid_login_error_message(self) -> str:
        return "Please enter the correct one-time password."


class EmailAuthForm(BaseAuthForm):
    email = forms.EmailField()
    password = forms.CharField(strip=False)

    def get_invalid_login_error_message(self):
        return (
            "Please enter a correct username and password. Note that both"
            " fields are case-sensitive."
        )


class UsernameAuthForm(BaseAuthForm):
    username = UsernameField()
    password = forms.CharField(strip=False)
    class_id = forms.CharField(
        validators=[
            RegexValidator(
                r"^[A-Z]{2}([0-9]{3}|[A-Z]{3})$",
                (
                    "Must be 5 upper case letters or 2 upper case letters"
                    " followed by 3 digits"
                ),
            ),
        ],
    )

    def get_invalid_login_error_message(self):
        return (
            "Please enter a correct username and password for a class."
            " Double check your class ID is correct and remember that your"
            " username and password are case-sensitive."
        )


class UserIdAuthForm(BaseAuthForm):
    user_id = forms.IntegerField(min_value=1)
    login_id = forms.CharField(min_length=32, max_length=32)

    def get_invalid_login_error_message(self):
        return (
            "Your login link is invalid. Please contact your teacher or the"
            " Code for Life team for support."
        )
