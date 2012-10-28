from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('django_actions.views',
    url(r'^act/(?P<app_n_model>[\w\.]+)/$', 'act', name='url_act'),
)
