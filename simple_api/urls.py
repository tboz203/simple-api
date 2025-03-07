"""URL configuration for Simple-API."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("classes", views.ClassViewSet)
router.register("teachers", views.TeacherViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
