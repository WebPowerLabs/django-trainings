from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from courses import views

urlpatterns = patterns('',
   url('^add_favourite/(?P<pk>[-\w]+)$', login_required(
                                    views.CourseFavouriteAddView.as_view()),
                                    name='add_favourite'),
    url('^order/$', staff_member_required(views.CourseOrderView.as_view()),
                                                                 name='order'),
    url('^$', views.CourseListView.as_view(), name='list'),
    url('^(?P<slug>[-\w]+)/$', views.CourseDetailView.as_view(),
                                                                name='detail'),
    url('^(?P<slug>[-\w]+)/delete/$', staff_member_required(
                                             views.CourseDeleteView.as_view()),
                                                                name='delete'),
)
