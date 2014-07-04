try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from dtf_comments import views

urlpatterns = patterns('dtf_comments.views',
#     url(r'^share/$', 'c_share', name='share'),

    url('^share/$', views.DTFCommentShareView.as_view(), name='share'),
)
