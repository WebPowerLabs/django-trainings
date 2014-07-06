try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from dtf_comments import views

urlpatterns = patterns('dtf_comments.views',
    url('^share/(?P<content_pk>[-\w]+)$', views.DTFCommentShareView.as_view(),
        name='share'),
    url(r'^preview_comment/$', views.CommentPreviewView.as_view(),
        name='preview_comment'),
)
