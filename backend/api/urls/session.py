from django.urls import path, re_path

from ..views.session import ClearExpiredView, LoginView

urlpatterns = [
    re_path(
        r"^login/(?P<form>email|username|user-id|otp)/$",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "clear-expired/",
        ClearExpiredView.as_view(),
        name="clear-expired-sessions",
    ),
]
