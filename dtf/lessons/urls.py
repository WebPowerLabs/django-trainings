from django.contrib.admin.views.decorators import staff_member_required

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here
from lessons import views

urlpatterns = patterns('',
    url('^order/(?P<course_pk>[-\w]+)$', staff_member_required(
                               views.LessonOrderView.as_view()), name='order'),
    url('^$', views.LessonListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/(?P<tag_id>\d+)?$',
                              views.LessonDetailView.as_view(), name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', staff_member_required(
                             views.LessonDeleteView.as_view()), name='delete'),
    url('^add/(?P<slug>[-\w]+)/$', staff_member_required(
                                   views.LessonAddView.as_view()), name='add'),

)
