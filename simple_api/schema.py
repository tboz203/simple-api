"""Strawberry GraphQL types for Simple-API."""

import strawberry
import strawberry_django
from strawberry import auto
from strawberry_django.optimizer import DjangoOptimizerExtension

from . import models

IDFilterLookup = strawberry_django.BaseFilterLookup[strawberry.ID]


@strawberry_django.filter(models.Class, lookups=True)
class ClassFilter:
    id: auto
    name: auto
    maximum_capacity: auto
    current_capacity: int | None
    teacher: "TeacherFilter | None"
    students: "StudentFilter | None"


@strawberry_django.type(models.Class, filters=ClassFilter)
class Class:
    id: auto
    name: auto
    maximum_capacity: auto
    current_capacity: auto
    teacher: "Teacher"
    students: list["Student"]


@strawberry_django.filter(models.Person, lookups=True)
class TeacherFilter:
    id: auto
    name: auto
    phone: auto

    classes: ClassFilter | None = strawberry_django.field(field_name="classes_teaching")


@strawberry_django.type(models.Person, filters=TeacherFilter)
class Teacher:
    id: auto
    name: auto
    phone: auto

    classes: auto = strawberry_django.field(field_name="classes_teaching")

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.distinct().filter(classes_teaching__isnull=False)


@strawberry_django.filter(models.Person, lookups=True)
class StudentFilter:
    id: auto
    name: auto
    phone: auto

    classes: ClassFilter | None = strawberry_django.field(field_name="classes_attending")


@strawberry_django.type(models.Person, fields="__all__", filters=StudentFilter)
class Student:
    classes: list[Class] = strawberry_django.field(field_name="classes_attending")

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.distinct().filter(classes_attending__isnull=False)


@strawberry.type
class Query:
    classes: list[Class] = strawberry_django.field()
    class_: Class | None = strawberry_django.field(name="class")
    teachers: list[Teacher] = strawberry_django.field()
    teacher: Teacher | None = strawberry_django.field()
    students: list[Student] = strawberry_django.field()
    student: Student | None = strawberry_django.field()


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
