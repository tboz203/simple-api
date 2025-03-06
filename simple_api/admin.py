"""Admin site configuration for Simple-API."""

from django.contrib import admin

from .models import Class, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name", "phone"]


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ["name", "teacher", "current_capacity", "maximum_capacity"]
