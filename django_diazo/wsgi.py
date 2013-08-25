import os
from logging import getLogger
from diazo.wsgi import DiazoMiddleware
from utils import theme_path, theme_url, get_active_theme


class DiazoMiddlewareWrapper(object):
    def __init__(self, app):
        self.app = app
        self.theme_id = None

    def __call__(self, environ, start_response):
        theme = get_active_theme()
        if theme:
            rules_file = os.path.join(theme_path(theme), 'rules.xml')
            if theme.id != self.theme_id or not os.path.exists(rules_file) or theme.debug:
                fp = open(rules_file, 'w')
                try:
                    if theme.rules:
                        fp.write(theme.rules.serialize())
                finally:
                    fp.close()

                self.theme_id = theme.id

            self.diazo = DiazoMiddleware(
                app=self.app,
                global_conf=None,
                rules=rules_file,
                prefix=theme_url(theme),
            )
            try:
                return self.diazo(environ, start_response)
            except Exception, e:
                getLogger('django_diazo').error(e)

        return self.app(environ, start_response)
