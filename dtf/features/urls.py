try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('features.views',
    url(r'^add/$', 'feature_create', name='add'),
    url(r'^add/(?P<object_pk>.+)/(?P<class_name>.+)/$', 'feature_create_comment', name='add_comment'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='redirect'),
)