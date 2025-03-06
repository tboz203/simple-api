"""View definitions for Simple-API."""

from django.http import HttpRequest
from ninja import NinjaAPI

from . import schemas
from .models import Class, Person

api = NinjaAPI()


@api.get("/classes/", response=list[schemas.ClassTeacherSchema])
def get_classes(request: HttpRequest) -> list[schemas.ClassTeacherSchema]:
    return [schemas.ClassTeacherSchema.from_orm(cls) for cls in Class.objects.all()]


@api.get("/classes/{name}/", response=schemas.ClassDetailSchema)
def get_class_by_name(request: HttpRequest, name: str) -> schemas.ClassDetailSchema:
    return schemas.ClassDetailSchema.from_orm(Class.objects.get(name=name))


@api.get("/teachers/", response=list[schemas.TeacherClassSchema])
def get_teachers(request: HttpRequest) -> list[schemas.TeacherClassSchema]:
    return [
        schemas.TeacherClassSchema.from_orm(teacher)
        for teacher in Person.objects.filter(classes_teaching__isnull=False)
    ]
