try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from courses import views

urlpatterns = patterns('',
        url('^delete_history/(?P<pk>[-\w]+)/$',
                                    views.CourseHistoryDeleteView.as_view(),
                                                        name='delete_history'),
    url('^history/$', views.CourseHistoryListView.as_view(),
                                                        name='history'),
    url('^favourite_action/(?P<pk>[-\w]+)/$',
           views.CourseFavouriteActionView.as_view(), name='favourite_action'),
    url('^order/$', views.CourseOrderView.as_view(), name='order'),
    url('^favourites/$', views.CourseFavouriteListView.as_view(),
                                                        name='favourites'),
    url('^$', views.CourseListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/$', views.CourseDetailView.as_view(),
                                                                name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', views.CourseDeleteView.as_view(),
                                                                name='delete'),

)

