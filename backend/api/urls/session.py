from django.contrib.auth.views import LogoutView
from django.urls import path

from ..views.session import ClearExpiredView, LoginView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "clear-expired/",
        ClearExpiredView.as_view(),
        name="clear-expired-sessions",
    ),
]
