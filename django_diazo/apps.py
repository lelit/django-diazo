import imp
from django.apps import AppConfig
from django.conf import settings

from django_diazo.settings import MODULE_NAME


class DjangoDiazoConfig(AppConfig):
    name = 'django_diazo'
    label = 'django_diazo'
    verbose_name = "Django Diazo"

    def ready(self):
        """
        Implement this method to run code when Django starts.
        Autodiscovers the 'diazo' module in project apps.
        """
        for app in settings.INSTALLED_APPS:
            try:
                app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
            except AttributeError:
                continue

            try:
                imp.find_module(MODULE_NAME, app_path)
            except ImportError:
                continue
            __import__('%s.%s' % (app, MODULE_NAME))
