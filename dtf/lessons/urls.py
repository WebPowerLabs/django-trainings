try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here
from lessons import views

urlpatterns = patterns('',
    url('^upload_video_file/$', views.UploadVideoFileView.as_view(),
                                                    name='upload_video_file'),
    url('^delete_history/(?P<pk>[-\w]+)/$',
                                    views.LessonHistoryDeleteView.as_view(),
                                                        name='delete_history'),
    url('^history/$', views.LessonHistoryListView.as_view(),
                                                        name='history'),
    url('^favourites/$', views.LessonFavouriteListView.as_view(),
                                                        name='favourites'),
    url('^favourite_action/(?P<slug>[-\w]+)$',
                                    views.LessonFavouriteActionView.as_view(),
                                                    name='favourite_action'),
    url('^order/(?P<slug>[-\w]+)$', views.LessonOrderView.as_view(),
                                                                name='order'),
    url('^$', views.LessonListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/(?P<tag_id>\d+)?$',
                            views.LessonDetailView.as_view(), name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', views.LessonDeleteView.as_view(),
                                                                name='delete'),
    url('^add/(?P<slug>[-\w]+)/$', views.LessonAddView.as_view(), name='add'),
    url('^complete_action/(?P<slug>[-\w]+)$',
                                    views.LessonCompleteActionView.as_view(),
                                                    name='complete_action'),
                       
)
