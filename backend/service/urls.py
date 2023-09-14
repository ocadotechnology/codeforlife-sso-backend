"""service URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from rest_framework import status

urlpatterns = [
    path(
        settings.SERVICE_BASE_URL,
        include(
            [
                path("admin/", admin.site.urls),
                path("api/", include("api.urls")),
                re_path(
                    r".*",
                    # lambda request: render(request, "frontend.html"),
                    lambda request: HttpResponse(
                        "TODO: relocate login pages to sso service and redirect to them"
                    ),
                    name="frontend",
                ),
            ]
        ),
    ),
    re_path(
        r".*",
        lambda request: HttpResponse(
            f'Service not found. The base URL is "{settings.SERVICE_BASE_URL}".',
            status=status.HTTP_404_NOT_FOUND,
        ),
        name="no-service",
    ),
]
