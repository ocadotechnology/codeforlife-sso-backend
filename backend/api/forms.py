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


class EmailAuthForm(BaseAuthForm):
    email = forms.EmailField()
    password = forms.CharField(strip=False)

    def get_invalid_login_error_message(self):
        return (
            "Please enter a correct username and password. Note that both"
            " fields may be case-sensitive."
        )


class UsernameAuthForm(BaseAuthForm):
    username = UsernameField()
    password = forms.CharField(strip=False)
    class_id = forms.CharField(
        validators=[
            RegexValidator(
                r"^[A-Z]{2}[0-9]{3}$",
                "Must be 2 upper case letters followed by 3 digits",
            ),
        ],
    )


class UserIdAuthForm(BaseAuthForm):
    user_id = forms.IntegerField(min_value=1)
    login_id = forms.CharField(min_length=32, max_length=32)
