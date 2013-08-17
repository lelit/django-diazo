from django.conf import settings
from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'rules/$', views.rules, name='rules'),
    url(r'rules/(?P<slug>[0-9A-Za-z-_.//]+)/$', views.static, name='static-by-slug') if settings.APPEND_SLASH else
    url(r'rules/(?P<slug>[0-9A-Za-z-_.//]+)$', views.static, name='static-by-slug')
)
