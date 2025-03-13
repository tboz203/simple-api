"""Strawberry GraphQL types for Simple-API."""

import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from . import models


@strawberry_django.filter(models.Class, lookups=True)
class ClassFilter:
    id: strawberry.ID | None
    name: str | None
    maximum_capacity: int | None
    current_capacity: int | None
    teacher: "TeacherFilter | None"
    students: "StudentFilter | None"


@strawberry_django.type(models.Class, filters=ClassFilter)
class Class:
    id: strawberry.ID
    name: str
    maximum_capacity: int
    current_capacity: int
    teacher: "Teacher"
    students: list["Student"]


@strawberry_django.filter(models.Person, lookups=True)
class TeacherFilter:
    id: strawberry.ID | None
    name: str | None
    phone: str | None

    classes: "ClassFilter | None" = strawberry_django.field(field_name="classes_teaching")


@strawberry_django.type(models.Person, filters=TeacherFilter)
class Teacher:
    id: strawberry.ID
    name: str
    phone: str

    classes: list[Class] = strawberry_django.field(field_name="classes_teaching")

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.filter(classes_teaching__isnull=False)


@strawberry_django.filter(models.Person, lookups=True)
class StudentFilter:
    id: strawberry.ID | None
    name: str | None
    phone: str | None

    classes: "ClassFilter | None" = strawberry_django.field(field_name="classes_attending")


@strawberry_django.type(models.Person, fields="__all__", filters=StudentFilter)
class Student:
    classes: list[Class] = strawberry_django.field(field_name="classes_attending")

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.filter(classes_attending__isnull=False)


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
