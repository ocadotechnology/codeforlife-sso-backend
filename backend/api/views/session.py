from django.contrib.auth.views import (
    LoginView as _LoginView,
    LogoutView as _LogoutView,
)


class LoginView(_LoginView):
    pass


class LogoutView(_LogoutView):
    pass
