"""API Manager class for Simple-API."""


from django.conf import settings
from ninja import NinjaAPI


class ApiManager(NinjaAPI):
    """A wrapper around `ninja.NinjaAPI` to let me do some things my way."""

    @property
    def title(self):
        return settings.APP_NAME

    @property
    def version(self):
        return settings.APP_VERSION

    @property
    def description(self):
        return settings.APP_DESCRIPTION

    title = title.setter(lambda self, _: None)
    version = version.setter(lambda self, _: None)
    description = description.setter(lambda self, _: None)
