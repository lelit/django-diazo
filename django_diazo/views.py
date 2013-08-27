from django.views.generic import View, RedirectView


class DiazoEnableThemeView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session.pop('theme_enabled')
        return super(DiazoEnableThemeView, self).dispatch(request, *args, **kwargs)


class DiazoDisableThemeView(View):
    def dispatch(self, request, *args, **kwargs):
        request.session['theme_enabled'] = False
        return super(DiazoDisableThemeView, self).dispatch(request, *args, **kwargs)


class DiazoEnableThemeRedirectView(DiazoEnableThemeView, RedirectView):
    pass


class DisableThemeRedirectView(DiazoDisableThemeView, RedirectView):
    pass
