from django.urls import path

from ..views.session import ClearExpiredView, LoginView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "clear-expired/",
        ClearExpiredView.as_view(),
        name="clear-expired-sessions",
    ),
]
