import os
import zipfile
from codemirror.widgets import CodeMirrorTextarea
from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from actions import enable_theme
from models import Theme


class ThemeForm(forms.ModelForm):
    upload = forms.FileField(required=False, label=_('Zip file'),
                             help_text=_('Will be unpacked in media directory.'))
    codemirror = CodeMirrorTextarea(mode="xml", theme="eclipse", config={ 'fixedGutter': True })
    rules_editor = forms.CharField(required=False, widget=codemirror)

    class Meta:
        model = Theme

    def __init__(self, *args, **kwargs):
        if not 'initial' in kwargs:
            kwargs['initial'] = {}
        if 'instance' in kwargs and kwargs['instance']:
            rules = os.path.join(format(settings.MEDIA_ROOT), kwargs['instance'].prefix, 'rules.xml')
            fp = open(rules)
            kwargs['initial'].update({'rules_editor': fp.read()})
            fp.close()
        super(ThemeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if 'upload' in self.files:
            f = self.files['upload']
            if zipfile._check_zipfile(f):
                # Unzip uploaded theme
                z = zipfile.ZipFile(f)
                z.extractall(os.path.join(format(settings.MEDIA_ROOT), os.path.splitext(z.filename)[0]))
                # Set prefix dir
                self.instance.prefix = os.path.splitext(z.filename)[0]

        rules = os.path.join(format(settings.MEDIA_ROOT), self.instance.prefix, 'rules.xml')
        fp = open(rules, 'w')
        fp.write(self.cleaned_data['rules_editor'])
        fp.close()

        if self.cleaned_data['enabled']:
            for t in Theme.objects.all():
                t.enabled = False
                t.save()
        return super(ThemeForm, self).save(commit)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled',)
    actions = [enable_theme]
    form = ThemeForm

    def get_fieldsets(self, request, obj=None):
        "Hook for specifying fieldsets for the add form."
        upload_classes = ()
        editor_classes = ('collapse',)
        if obj:
            upload_classes = ('collapse',)
            editor_classes = ()
        return (
            (None, {'fields': ('name', 'prefix', 'enabled', 'debug',)}),
            (_('Upload theme'), {'classes': upload_classes, 'fields': ('upload',)}),
            (_('Rules editor'), {'classes': editor_classes, 'fields': ('rules_editor',)}),
        )


admin.site.register(Theme, ThemeAdmin)
