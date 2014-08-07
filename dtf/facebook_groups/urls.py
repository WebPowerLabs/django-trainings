try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# url(r'^comments/feeds/rss/$', LatestCommentFeed(), name="latest_comments_feed"),
urlpatterns = patterns('facebook_groups.views',
	url(r"^$", "fb_group_list", name="list"),
	url(r"^add/$", "fb_group_create", name="add"),
	url(r"^(?P<fb_uid>\d+)/$", "fb_group_detail", name="detail"),
	url(r"^(?P<fb_uid>\d+)/edit/$", "fb_group_edit", name="edit"),
	url(r"^(?P<fb_uid>\d+)/pin_comment/(?P<comment_id>\d+)/$", "pin_comment", name="pin_comment"),
	url(r"^(?P<fb_uid>\d+)/unpin_comment/$", "unpin_comment", name="unpin_comment"),
	url(r"^(?P<fb_uid>\d+)/feed/$", "fb_group_feed", name="feed"),
	url(r"^(?P<fb_uid>\d+)/post/$", "fb_group_feed_post", name="feed_post"),
	)
