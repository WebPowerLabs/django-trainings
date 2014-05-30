try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from resources import views

urlpatterns = patterns('',
    url('^$', views.ResourceListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/$', views.ResourceDetailView.as_view(),
                                                                name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', views.ResourceDeleteView.as_view(),
                                                                name='delete'),
    )
