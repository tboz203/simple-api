"""
Models for Simple-API.

This module contains a `Person` model (for modeling students and teachers), as
well as a `Class` model.
"""

from django.db import models


class Person(models.Model):
    """A model for Students and Teachers."""

    name = models.CharField(unique=True, max_length=64)
    phone = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "People"


class Class(models.Model):
    """A model for Classes."""

    name = models.CharField(unique=True, max_length=64)
    teacher = models.ForeignKey(Person, related_name="classes_teaching", on_delete=models.CASCADE)
    students = models.ManyToManyField(Person, related_name="classes_attending")
    maximum_capacity = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"

    @property
    def current_capacity(self):
        return self.maximum_capacity - self.students.count()
