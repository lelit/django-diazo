# Django Diazo

Integrate Diazo in Django using WSGI middleware and add/change themes using the Django Admin interface.

## Installation

### settings.py

    INSTALLED_APPS = (
        ...
        'django_diazo',
        ...
    )

Optionally you can add `DIAZO_INITIAL_RULES_FILE` and point to a file with an initial rules.xml template.
Example rules.xml contents:

    <?xml version="1.0" encoding="UTF-8"?>
    <rules
        xmlns="http://namespaces.plone.org/diazo"
        xmlns:css="http://namespaces.plone.org/diazo/css"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

        <!-- Disable theme for Django Admin -->
        <notheme if-path="admin" />

        <!-- Enable theme -->
        <theme href="index.html" />

    </rules>

### wsgi.py

    # Apply WSGI middleware here.
    from django_diazo.wsgi import DiazoMiddlewareWrapper
    application = DiazoMiddlewareWrapper(application)

### Database (South migrations)

    python manage.py migrate django_diazo

### Uploaded themes

By default, the .zip files that are uploaded are extracted in the media folder.
You might want to serve these files in debug mode.
Add the following to your `urls.py`:

    if settings.DEBUG:
        urlpatterns = patterns('',
           url(r'^media/themes/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': os.path.join(settings.MEDIA_ROOT, 'themes'), 'show_indexes': True}),
        ) + urlpatterns

For production environments it is not recommended to serve files from the media folder.
This implementation only servers files in the `themes` folder within the media folder but it would be better to
serve these files using a web server and not via Django.

### CodeMirror

Download [CodeMirror](http://codemirror.net/).

See https://pypi.python.org/pypi/django-codemirror-widget.

#### How to Use

Specify `CODEMIRROR_PATH` on `settings.py`.

`CODEMIRROR_PATH` is the URI of CodeMirror directory like `CODEMIRROR_PATH = r"javascript/codemirror"`.
If you don't specify it, it defaults to `'codemirror'`.

CodeMirror download should be put there (unpacked).

#### Settings

- `CODEMIRROR_PATH`
    - the URI of CodeMirror directory (your CodeMirror installation should live in `{{ STATIC_URL }}/{{ CODEMIRROR_PATH }}`)
- `CODEMIRROR_MODE`
    - the default mode which may be a string or configuration map (DEFAULT: 'javascript')
- `CODEMIRROR_THEME`
    - the default theme applied (DEFAULT: 'default')
- `CODEMIRROR_CONFIG`
    - base mapping for the rest of the CodeMirror options (DEFAULT: `{ 'lineNumbers': True }`)