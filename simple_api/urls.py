"""URL configuration for Simple-API."""

from django.contrib import admin
from django.urls import path

from .views import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
