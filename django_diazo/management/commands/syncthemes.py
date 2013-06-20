from django.conf import settings
from logging import getLogger
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django_diazo.models import Theme


class Command(BaseCommand):
    help = _('Synchronize database with built-in themes from the DIAZO_BUILTIN_THEMES setting.')
    requires_model_validation = True

    def handle(self, *args, **options):
        logger = getLogger('django_diazo')
        if hasattr(settings, 'DIAZO_BUILTIN_THEMES'):
            themes = dict([(slugify(t.name), t) for t in Theme.objects.filter(builtin=True)])
            # Add/modify themes
            for path, url, name in settings.DIAZO_BUILTIN_THEMES:
                slug = slugify(name)
                if slug not in themes:
                    Theme.objects.create(
                        name=name,
                        path=path,
                        url=url,
                        builtin=True
                    )
                    logger.info('Added new theme with name \'{0}\'.'.format(name))
                if slug in themes:
                    themes.pop(slug)
            # Delete themes
            for theme in themes:
                theme.delete()
        logger.info('Done syncing built-in themes')
