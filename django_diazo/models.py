from django.db import models
from django.utils.translation import ugettext_lazy as _


class Theme(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=True)
    rules = models.CharField(_('rules'), max_length=255, blank=True)
    prefix = models.CharField(_('prefix'), max_length=255, blank=True)
    enabled = models.BooleanField(_('enabled'), default=False)
    debug = models.BooleanField(_('debug'), default=False)

    def __unicode__(self):
        return self.name
