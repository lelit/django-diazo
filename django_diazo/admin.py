import os
import zipfile
from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from actions import enable_theme
from models import Theme


class ThemeForm(forms.ModelForm):
    upload = forms.FileField(required=False, label=_('Upload theme zip'), help_text=_('Will be unpacked in media directory.'))

    class Meta:
        model = Theme

    def save(self, commit=True):
        if 'upload' in self.files:
            f = self.files['upload']
            if zipfile._check_zipfile(f):
                # Unzip uploaded theme
                z = zipfile.ZipFile(f)
                z.extractall(os.path.join(format(settings.MEDIA_ROOT), os.path.splitext(z.filename)[0]))
                # Also set prefix dir
                self.instance.prefix = os.path.join(settings.MEDIA_URL[1:], os.path.splitext(z.filename)[0])
                # And rules.xml
                self.instance.rules = os.path.join(format(settings.MEDIA_ROOT), os.path.splitext(z.filename)[0], 'rules.xml')
                if not os.path.exists(self.instance.rules):
                    # Touch rules.xml since it doesn't exist
                    open(self.instance.rules, 'w').close()
        return super(ThemeForm, self).save(commit)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled',)
    actions = [enable_theme]
    form = ThemeForm


admin.site.register(Theme, ThemeAdmin)
