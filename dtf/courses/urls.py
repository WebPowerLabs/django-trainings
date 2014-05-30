try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from courses import views

urlpatterns = patterns('',
    url('^$', views.CourseListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/$', views.CourseDetailView.as_view(),
                                                                name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', views.CourseDeleteView.as_view(),
                                                                name='delete'),
)
