from django.db import models
from django.utils.translation import ugettext_lazy as _


class Theme(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=True)
    prefix = models.CharField(_('prefix'), max_length=255, blank=True)
    enabled = models.BooleanField(_('enabled'), default=False,
                                  help_text=_('Enable this theme (and disable the current, if enabled).'))
    debug = models.BooleanField(_('debug'), default=False,
                                help_text=_('Reload theme on every request (vs. reload on changing themes).'))

    def __unicode__(self):
        return self.name
