# Django Diazo

Integrate Diazo in Django using WSGI middleware and add/change themes using the Django Admin interface.

## Installation

### settings.py

    INSTALLED_APPS = (
        ...
        'django_diazo',
        ...
    )

### wsgi.py

    from django_diazo.wsgi import DiazoMiddlewareWrapper
    application = DiazoMiddlewareWrapper(application)

### South

    python manage.py migrate django_diazo
