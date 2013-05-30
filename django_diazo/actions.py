from django.utils.translation import ugettext_lazy as _
from models import Theme


def enable_theme(modeladmin, request, queryset):
    for t in Theme.objects.all():
        t.enabled = False
        t.save()
    for i in queryset:
        i.enabled = True
        i.save()
        break
enable_theme.short_description = _('Enable theme')
