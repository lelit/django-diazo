from django.conf import settings


MODULE_NAME = 'diazo'

DOCTYPE = getattr(
    settings,
    'DIAZO_DOCTYPE',
    None,
)

ALLOWED_CONTENT_TYPES = getattr(
    settings,
    'DIAZO_ALLOWED_CONTENT_TYPES',
    ['text/html', 'application/xhtml+xml', 'text/xml', 'application/xml'],
)
