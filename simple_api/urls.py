"""URL configuration for Simple-API."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("classes", views.ClassViewSet)
router.register("teachers", views.TeacherViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("", include(router.urls)),
]
