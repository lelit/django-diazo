import os
import zipfile
from codemirror.widgets import CodeMirrorTextarea
from django import forms
from django.contrib import admin
from django.forms import Widget
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from django_diazo.actions import enable_theme
from django_diazo.models import Theme
from django_diazo.utils import theme_path


class IFrameWidget(Widget):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'src': 'http://localhost:8000'}
        if attrs:
            default_attrs.update(attrs)
        super(IFrameWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        # import pdb;pdb.set_trace()
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html('<iframe{0} />',
                           forms.util.flatatt(final_attrs))


class ThemeForm(forms.ModelForm):
    upload = forms.FileField(required=False, label=_('Zip file'),
                             help_text=_('Will be unpacked in media directory.'))
    rules_editor = forms.CharField(required=False, widget=CodeMirrorTextarea())
    preview = forms.URLField(required=False, widget=IFrameWidget())

    class Meta:
        model = Theme

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance']:
            rules = os.path.join(theme_path(kwargs['instance']), 'rules.xml')

            if os.path.exists(rules):
                fp = open(rules)
                if not 'initial' in kwargs:
                    kwargs['initial'] = {'rules_editor': fp.read()}
                else:
                    kwargs['initial'].update({'rules_editor': fp.read()})
                fp.close()
        super(ThemeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ThemeForm, self).save(commit)
        instance.save()  # We need the pk

        if 'upload' in self.files:
            f = self.files['upload']
            if zipfile._check_zipfile(f):
                z = zipfile.ZipFile(f)
                # Unzip uploaded theme
                z.extractall(theme_path(instance))

        path = theme_path(instance)
        if not os.path.exists(path):
            os.makedirs(path)

        if instance.enabled:
            for t in Theme.objects.all():
                t.enabled = False
                t.save()
        return instance


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled',)
    actions = [enable_theme]
    form = ThemeForm

    def get_fieldsets(self, request, obj=None):
        """Hook for specifying fieldsets for the add form."""
        return (
            (None, {'fields': ('name', 'slug', 'prefix', 'rules', 'enabled', 'debug')}),
            (_('Built-in settings'), {'classes': ('collapse',), 'fields': ('path', 'url', 'builtin',)}),
            (_('Upload theme'), {'classes': ('collapse',), 'fields': ('upload',)}),
            # (_('Preview'), {'classes': (), 'fields': ('preview',)}),
            # (_('Rules editor'), {'classes': collapsed, 'fields': ('rules_editor',)}),
        )


admin.site.register(Theme, ThemeAdmin)
