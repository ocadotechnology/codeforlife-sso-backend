from django.urls import path, include

from .session import urlpatterns as session_urlpatterns

urlpatterns = [
    path("session/", include(session_urlpatterns)),
]
