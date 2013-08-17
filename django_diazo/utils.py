import os
from django.conf import settings
from .models import Theme


def get_active_theme():
    themes = Theme.objects.filter(enabled=True)
    if len(themes):
        return themes[0]
    return None

def theme_path(theme_instance):
    if theme_instance.builtin:
        return theme_instance.path
    else:
        return os.path.join(format(settings.MEDIA_ROOT), 'themes', str(theme_instance.pk))


def theme_url(theme_instance):
    if theme_instance.builtin:
        return theme_instance.url
    else:
        return '/'.join([format(settings.MEDIA_URL) + 'themes', str(theme_instance.pk), theme_instance.prefix])
