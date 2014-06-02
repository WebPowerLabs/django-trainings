try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('facebook_groups.views',
	url(r"^$", "fb_group_list", name="list"),
	url(r"^add/$", "fb_group_create", name="add"),
	url(r"^(?P<fb_uid>\d+)/$", "fb_group_detail", name="detail"),
	url(r"^(?P<fb_uid>\d+)/feed/$", "fb_group_feed", name="feed"),
	url(r"^(?P<fb_uid>\d+)/sync/$", "sync_fb_data", name="sync"),
	url(r"^(?P<fb_uid>\d+)/post/$", "fb_group_feed_post", name="feed_post"),
	)