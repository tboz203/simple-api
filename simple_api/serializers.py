"""Serializers for Simple-API."""

from collections.abc import Collection
from typing import no_type_check

from rest_framework import serializers

from .models import Class, Person


class SimpleAPISerializer(serializers.ModelSerializer):
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__ensure_id_excluded()

    @classmethod
    @no_type_check
    def __ensure_id_excluded(cls):
        """Ensure all SimpleAPISerializers exclude the `id` field."""

        if not hasattr(cls, "Meta"):
            raise AttributeError("SimpleAPISerializer Meta configuration subclass not found", cls)

        # if `id` is explicitly requested, we won't exclude it here
        if hasattr(cls.Meta, "fields") and "id" in cls.Meta.fields:
            return

        # ensure an `exclude` list is present
        if not hasattr(cls.Meta, "exclude"):
            cls.Meta.exclude = []
        elif isinstance(cls.Meta.exclude, Collection) and not isinstance(cls.Meta.exclude, str):
            cls.Meta.exclude = list(cls.Meta.exclude)

        # ensure `id` is excluded
        if isinstance(cls.Meta.exclude, list) and "id" not in cls.Meta.exclude:
            cls.Meta.exclude.append("id")


class SimplePersonSerializer(SimpleAPISerializer):
    """A 0-depth serializer for People (i.e. the Person model)."""

    class Meta:
        model = Person


class SimpleClassSerializer(SimpleAPISerializer):
    """A 0-depth serializer for Classes."""

    class Meta:
        model = Class
        exclude = ["teacher", "students"]


class ClassTeacherSerializer(SimpleAPISerializer):
    """A serializer for Classes that includes a Teacher."""

    teacher = SimplePersonSerializer()

    class Meta:
        model = Class
        exclude = ["students"]


class TeacherClassSerializer(SimpleAPISerializer):
    """
    A serializer for Teachers that includes Classes.

    (Teachers are People who are the teacher of at least one class).
    """

    classes = SimpleClassSerializer(source="classes_teaching", many=True)

    class Meta:
        model = Person


class ClassDetailSerializer(SimpleAPISerializer):
    teacher = SimplePersonSerializer()
    students = SimplePersonSerializer(many=True)

    class Meta:
        model = Class
