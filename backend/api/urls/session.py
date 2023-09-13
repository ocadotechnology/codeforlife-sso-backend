from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from ..views.session import LoginView

urlpatterns = [
    re_path(
        r"^(?P<user_type>teacher|dependent_student|independent_student)/login/$",
        LoginView.as_view(),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
