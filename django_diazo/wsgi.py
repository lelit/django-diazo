import os
from logging import getLogger
from diazo.wsgi import DiazoMiddleware
from django.core.handlers.wsgi import WSGIRequest
from django_diazo.utils.common import get_active_theme, themes_enabled
from django_diazo.settings import DOCTYPE


class DiazoMiddlewareWrapper(object):
    """
    WSGI middleware wrapper for Diazo in Django.
    """
    def __init__(self, app):
        self.app = app
        self.theme_id = None
        self.diazo = None

    def __call__(self, environ, start_response):
        """
        This code will be executed every time a call is made to the server; on every request.
        When a theme is enabled, lookup the rules.xml file, overwrite the file when changes are made in the Django
        Admin interface (currently disabled) and initialize the DiazoMiddleware.
        When DiazoMiddleware fails, fall-back to the normal Django application and log the error.
        """
        request = WSGIRequest(environ)
        if themes_enabled(request):
            theme = get_active_theme(request)
            if theme:
                rules_file = os.path.join(theme.theme_path(), 'rules.xml')
                if theme.id != self.theme_id or not os.path.exists(rules_file) or theme.debug:
                    if not theme.builtin:
                        if theme.rules:
                            fp = open(rules_file, 'w')
                            try:
                                fp.write(theme.rules.serialize())
                            finally:
                                fp.close()

                    self.theme_id = theme.id

                    self.diazo = DiazoMiddleware(
                        app=self.app,
                        global_conf=None,
                        rules=rules_file,
                        prefix=theme.theme_url(),
                        doctype=DOCTYPE,
                    )
                try:
                    return self.diazo(environ, start_response)
                except Exception, e:
                    getLogger('django_diazo').error(e)

        return self.app(environ, start_response)
