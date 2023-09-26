from django.urls import include, path, re_path

from .views import ClearExpiredView, LoginView

urlpatterns = [
    path(
        "session/",
        include(
            [
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
        ),
    ),
]
