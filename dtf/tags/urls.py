try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from tags import views

urlpatterns = patterns('',
    url('^$', views.TagListView.as_view(), name='list'),
    url('^(?P<pk>[-\w]+)/$', views.TagDetailView.as_view(),
                                                                name='detail'),
    url('^(?P<pk>[-\w]+)/delete/$', views.TagDeleteView.as_view(),
                                                                name='delete'),
    )