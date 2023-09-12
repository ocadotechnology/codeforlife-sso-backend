from django.urls import include, path

from .cron import urlpatterns as cron_urlpatterns
from .csrf import urlpatterns as csrf_urlpatterns
from .session import urlpatterns as session_urlpatterns

urlpatterns = [
    path("cron/", include(cron_urlpatterns)),
    path("csrf/", include(csrf_urlpatterns)),
    path("session/", include(session_urlpatterns)),
]
