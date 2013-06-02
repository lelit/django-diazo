import os
from diazo.wsgi import DiazoMiddleware
from django.conf import settings
from models import Theme


class DiazoMiddlewareWrapper(object):
    def __init__(self, app):
        self.app = app
        self.theme_id = None

    def __call__(self, environ, start_response):
        for theme in Theme.objects.filter(enabled=True):
            if theme.id != self.theme_id or theme.debug:
                self.theme_id = theme.id
                self.diazo = DiazoMiddleware(
                    app=self.app,
                    global_conf=None,
                    rules=os.path.join(format(settings.MEDIA_ROOT), theme.prefix, 'rules.xml'),
                    prefix=os.path.join(format(settings.MEDIA_URL), theme.prefix)
                )
            try:
                return self.diazo(environ, start_response)
            except:
                return self.app(environ, start_response)
        return self.app(environ, start_response)
