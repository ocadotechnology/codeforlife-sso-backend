from django import forms
from django.contrib.auth.forms import UsernameField
from django.core.validators import RegexValidator


class CredentialsForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False)


class OneTimePasswordForm(forms.Form):
    otp = forms.CharField(
        validators=[
            RegexValidator(r"^[0-9]{6}$", "Must be 6 digits"),
        ],
    )


class DependentStudentAuthForm(forms.Form):
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
