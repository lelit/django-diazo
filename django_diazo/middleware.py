from cms.constants import RIGHT
from cms.toolbar.items import TemplateItem
import os
from lxml import etree
from logging import getLogger
from diazo.wsgi import DiazoMiddleware, asbool, DIAZO_OFF_HEADER
from diazo.utils import quote_param
from django.http import HttpResponse
from lxml.etree import tostring
from repoze.xmliter.serializer import XMLSerializer

from django_diazo.settings import DOCTYPE, ALLOWED_CONTENT_TYPES
from django_diazo.utils import get_active_theme, check_themes_enabled


class DjangoCmsDiazoMiddleware(object):
    """
    Django CMS 3 add-on
    """

    def process_request(self, request):
        """
        Add Django CMS 3 on/off switch to toolbar
        """
        if hasattr(request, 'toolbar'):
            request.toolbar.add_item(
                TemplateItem(
                    "cms/toolbar/items/on_off.html",
                    extra_context={
                        'request': request,
                        'diazo_enabled': check_themes_enabled(request),
                    },
                    side=RIGHT,
                ),
                len(request.toolbar.right_items),
            )


class DjangoDiazoMiddleware(object):
    """
    Django middleware wrapper for Diazo in Django.
    """

    def __init__(self):
        self.app = None
        self.theme_id = None
        self.diazo = None
        self.transform = None
        self.params = {}

    def should_transform(self, response):
        """
        Determine if we should transform the response
        """

        if asbool(response.get(DIAZO_OFF_HEADER, 'no')):
            return False

        content_type = response.get('Content-Type', '')
        if not content_type:
            return False

        no_diazo = True
        for content_type in ALLOWED_CONTENT_TYPES:
            if content_type in response.get('Content-Type', ''):
                no_diazo = False
                break
        if no_diazo:
            return False

        content_encoding = response.get('Content-Encoding')
        if content_encoding in ('zip', 'deflate', 'compress',):
            return False

        if 300 <= response.status_code <= 399 or response.status_code in [204, 401]:
            return False

        if len(response.content) == 0:
            return False

        return True

    def process_response(self, request, response):
        """
        Transform the response with Diazo if transformable
        """

        if not self.should_transform(response):
            return response

        content = response
        if check_themes_enabled(request):
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
                    compiled_theme = self.diazo.compile_theme()
                    self.transform = etree.XSLT(compiled_theme, access_control=self.diazo.access_control)
                    self.params = {}
                    for key, value in self.diazo.environ_param_map.items():
                        if key in request.environ:
                            if value in self.diazo.unquoted_params:
                                self.params[value] = request.environ[key]
                            else:
                                self.params[value] = quote_param(request.environ[key])

                try:
                    if isinstance(response, etree._Element):
                        response = HttpResponse()
                    else:
                        parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
                        content = etree.fromstring(response.content, parser)
                    result = self.transform(content, **self.params)
                    response.content = XMLSerializer(result, doctype=DOCTYPE).serialize()
                except Exception, e:
                    getLogger('django_diazo').error(e)
        if isinstance(response, etree._Element):
            response = HttpResponse('<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(content))
        return response
