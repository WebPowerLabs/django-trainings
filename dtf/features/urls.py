try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('features.views',
    url(r'^post/$',          'post',       name='post'),
    url(r'^delete/(\d+)/$',  'moderation.delete',           name='delete'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='redirect'),
)