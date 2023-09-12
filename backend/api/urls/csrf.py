from django.urls import path

from ..views.csrf import CookieView

# TODO: import these url patterns form codeforlife package.
urlpatterns = [
    path("cookie/", CookieView.as_view(), name="get-csrf-cookie"),
]
