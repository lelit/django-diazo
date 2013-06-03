import os
from django.conf import settings


def theme_path(theme_instance):
    return os.path.join(format(settings.MEDIA_ROOT), 'themes', str(theme_instance.pk))


def theme_url(theme_instance):
    return '/'.join([format(settings.MEDIA_URL) + 'themes', str(theme_instance.pk)])
