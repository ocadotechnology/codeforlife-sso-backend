from django.http import HttpResponse
from django.urls import include, path, re_path
from rest_framework import status

from .csrf import urlpatterns as csrf_urlpatterns
from .session import urlpatterns as session_urlpatterns

urlpatterns = [
    path("csrf/", include(csrf_urlpatterns)),
    path("session/", include(session_urlpatterns)),
    re_path(
        r".*",
        lambda request: HttpResponse(
            "API endpoint not found",
            status=status.HTTP_404_NOT_FOUND,
        ),
    ),
]
