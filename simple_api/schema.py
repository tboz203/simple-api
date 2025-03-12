"""A Graphene schema for Simple-API."""

from graphene import Field, Int, Interface, List, NonNull, ObjectType, Schema, String
from graphene_django import DjangoListField, DjangoObjectType

from . import models


class Class(DjangoObjectType):
    teacher = NonNull(lambda: Teacher)
    students = DjangoListField(lambda: Student)
    current_capacity = NonNull(Int)

    class Meta:
        model = models.Class
        fields = ("name", "maximum_capacity", "current_capacity", "students", "teacher")


class Person(Interface):
    name = NonNull(String)
    phone = NonNull(String)
    classes = List(NonNull(Class))


class Teacher(DjangoObjectType):
    classes = DjangoListField(Class, source="classes_teaching")

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(classes_teaching__isnull=False)

    class Meta:
        model = models.Person
        interfaces = [Person]
        fields = ["name", "phone", "classes"]


class Student(DjangoObjectType):
    classes = DjangoListField(Class, source="classes_attending")

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(classes_attending__isnull=False)

    class Meta:
        model = models.Person
        interfaces = [Person]
        fields = ["name", "phone", "classes"]


class Query(ObjectType):
    teachers = DjangoListField(Teacher)
    teacher = Field(Teacher, args={"name": NonNull(String)})
    students = DjangoListField(Student)
    student = Field(Student, args={"name": NonNull(String)})
    classes = DjangoListField(Class)
    class_ = Field(Class, name="class", args={"name": NonNull(String)})


schema = Schema(query=Query)
