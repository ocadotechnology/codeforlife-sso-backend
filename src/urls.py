"""
© Ocado Group
Created on 02/07/2024 at 12:16:48(+01:00).

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from codeforlife.urls import get_urlpatterns
from django.urls import include, path, re_path

from .views import ClearExpiredView, LoginOptionsView, LoginView

urlpatterns = get_urlpatterns([
    path(
        "session/",
        include(
            [
                path(
                    "login/",
                    include(
                        [
                            path(
                                "options/",
                                LoginOptionsView.as_view(),
                                name="login-options",
                            ),
                            re_path(
                                r"^(?P<form>email|username|user-id|otp|otp-bypass-token)/$",
                                LoginView.as_view(),
                                name="login",
                            ),
                        ]
                    ),
                ),
                path(
                    "clear-expired/",
                    ClearExpiredView.as_view(),
                    name="clear-expired-sessions",
                ),
            ]
        ),
    ),
])
