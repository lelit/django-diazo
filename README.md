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

    # Apply WSGI middleware here.
    from django_diazo.wsgi import DiazoMiddlewareWrapper
    application = DiazoMiddlewareWrapper(application)

### Database (South migrations)

    python manage.py migrate django_diazo

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