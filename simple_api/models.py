"""
Models for Simple-API.

This module contains a `Person` model (for modeling students and teachers), as
well as a `Class` model.
"""

from functools import cached_property

from django.db import models


class Person(models.Model):
    """A model for Students and Teachers."""

    name = models.CharField(unique=True, max_length=64)
    phone = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "People"


class _ClassManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().annotate(current_capacity=models.F("maximum_capacity") - models.Count("students"))
        )


class Class(models.Model):
    """A model for Classes."""

    name = models.CharField(unique=True, max_length=64)
    teacher = models.ForeignKey(Person, related_name="classes_teaching", on_delete=models.CASCADE)
    students = models.ManyToManyField(Person, related_name="classes_attending")
    maximum_capacity = models.PositiveIntegerField(default=30)

    objects = _ClassManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Classes"

    @cached_property
    def current_capacity(self) -> int:
        return self.maximum_capacity - self.students.count()
