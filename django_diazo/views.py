from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django_diazo.utils import get_active_theme


def rules(request, *args, **kwargs):
    theme = get_active_theme()
    if theme.rules:
        return HttpResponse(theme.rules.serialize())
    return HttpResponse('')


def static(request, slug, *args, **kwargs):
    return redirect(settings.STATIC_URL + slug)
