"""Django-Ninja schema definitions for Simple-API."""

from ninja import ModelSchema
from pydantic import Field

from .models import Class, Person


class SimplePersonSchema(ModelSchema):
    """An unnested schema for People (i.e. the Person model)."""

    class Meta:
        model = Person
        exclude = ["id"]


class SimpleClassSchema(ModelSchema):
    """An unnested schema for Classes."""

    current_capacity: int

    class Meta:
        model = Class
        exclude = ["id", "teacher", "students"]


class ClassTeacherSchema(ModelSchema):
    """A schema for Classes that includes a Teacher."""

    teacher: SimplePersonSchema

    class Meta:
        model = Class
        exclude = ["id", "students"]


class TeacherClassSchema(ModelSchema):
    """
    A schema for Teachers that includes Classes.

    (Teachers are People who are the teacher of at least one class).
    """

    classes: list[SimpleClassSchema] = Field(alias="classes_teaching")

    class Meta:
        model = Person
        exclude = ["id"]


class ClassDetailSchema(ModelSchema):
    """A schema for Classes that includes Teacher and Students."""

    teacher: SimplePersonSchema
    students: list[SimplePersonSchema]
    current_capacity: int

    class Meta:
        model = Class
        exclude = ["id"]
