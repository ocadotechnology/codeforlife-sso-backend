"""
© Ocado Group
Created on 01/12/2023 at 16:02:53(+00:00).
"""

from codeforlife.urls import get_urlpatterns

# pylint: disable-next=wildcard-import,unused-wildcard-import
from codeforlife.urls.handlers import *
from django.urls import include, path, re_path

from .views import LoginView

urlpatterns = get_urlpatterns(
    [
        path(
            "session/",
            include(
                [
                    re_path(
                        # pylint: disable-next=line-too-long
                        r"^(?P<form>login-with-email|login-with-otp|login-with-otp-bypass-token|login-as-student|auto-login-as-student|login-with-google)/$",
                        LoginView.as_view(),
                        name="session-login",
                    ),
                ]
            ),
        )
    ],
    include_user_urls=False,
)
