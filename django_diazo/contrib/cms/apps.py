from django.apps import AppConfig


class DjangoCmsDiazoConfig(AppConfig):
    name = 'django_diazo.contrib.cms'
    label = 'django_cms_diazo'
    verbose_name = "DjangoCMS Diazo"

    def ready(self):
        """
        Implement this method to run code when Django starts.
        """
