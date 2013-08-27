from django.views.generic import View, RedirectView


class DiazoEnableThemeView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session.pop('django_diazo_theme_enabled')
        return super(DiazoEnableThemeView, self).dispatch(request, *args, **kwargs)


class DiazoDisableThemeView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session['django_diazo_theme_enabled'] = False
        return super(DiazoDisableThemeView, self).dispatch(request, *args, **kwargs)


class DiazoEnableThemeRedirectView(DiazoEnableThemeView, RedirectView):
    pass


class DiazoDisableThemeRedirectView(DiazoDisableThemeView, RedirectView):
    pass
