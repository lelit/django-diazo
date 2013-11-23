import os
from logging import getLogger
from diazo.wsgi import DiazoMiddleware
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django_diazo.utils import get_active_theme
from django_diazo.settings import DOCTYPE


def themes_enabled(request):
        """
        Check if themes are enabled for the current session/request.
        """
        if settings.DEBUG and request.GET.get('theme') == 'none':
            return False
        if 'sessionid' not in request.COOKIES:
            return True
        session = SessionStore(session_key=request.COOKIES['sessionid'])
        return session.get('django_diazo_theme_enabled', True)


def get_diazo_middleware(app, request, last_enabled_theme_id):
    """
    Get the Diazo theme that is enabled and return the WSGI app.
    If no theme enabled or
    """
    if themes_enabled(request):
        theme = get_active_theme(request)
        if theme:
            rules_file = os.path.join(theme.theme_path(), 'rules.xml')
            if theme.id != last_enabled_theme_id or not os.path.exists(rules_file) or theme.debug:
                return (
                    theme.id,
                    DiazoMiddleware(
                        app=app,
                        global_conf=None,
                        rules=rules_file,
                        prefix=theme.theme_url(),
                        doctype=DOCTYPE,
                    ),
                )
    return None, app


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
        self.theme_id, self.diazo = get_diazo_middleware(self.app, request, self.theme_id)
        if self.theme_id:
            try:
                return self.diazo(environ, start_response)
            except Exception, e:
                getLogger('django_diazo').error(e)
        return self.app(environ, start_response)
