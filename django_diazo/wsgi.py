from logging import getLogger
from diazo.wsgi import DiazoMiddleware
from utils import theme_path, theme_url, get_active_theme


class DiazoMiddlewareWrapper(object):
    def __init__(self, app):
        self.app = app
        self.theme_id = None

    def __call__(self, environ, start_response):
        theme = get_active_theme()
        if theme and (theme.id != self.theme_id or theme.debug):
            self.theme_id = theme.id
            self.diazo = DiazoMiddleware(
                app=self.app,
                global_conf=None,
                rules='http://localhost:8000/diazo/rules/',
                prefix=theme_url(theme),
                read_file=False,
                read_network=True,
            )
            if 'HTTP_COOKIE' in environ:  # HTTP_COOKIE is only supplied in the original request
                try:
                    return self.diazo(environ, start_response)
                except Exception, e:
                    getLogger('django_diazo').error(e)
        return self.app(environ, start_response)
