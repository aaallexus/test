from datetime import timedelta

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import ugettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

from .utils import format_lazy

USER_SETTINGS = getattr(settings, 'REST_API_V1', None)

DEFAULTS = {

    'SEND_ACTIVATION_EMAIL': False,
}

IMPORT_STRINGS = (

)

REMOVED_SETTINGS = (

)


class APISettings(_APISettings):  # pragma: no cover
    def __check_user_settings(self, user_settings):
        # if we will have complicated settings we would have to make an http page with items descriptions
        # SETTINGS_DOC = 'https://github.com/..../somepage#settings'
        SETTINGS_DOC = 'project wiki'

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(format_lazy(
                    _("The '{}' setting has been removed. Please refer to '{}' for available settings."),
                    setting, SETTINGS_DOC,
                ))

        return user_settings


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'REST_API_V1':
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)