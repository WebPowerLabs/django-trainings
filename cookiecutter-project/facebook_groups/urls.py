try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('facebook_groups.views',
	url(r"^(?P<fb_uid>\d+)/$", "fb_group_feed", name="feed"),
	url(r"^(?P<fb_uid>\d+)/sync/$", "sync_fb_data", name="sync"),
	)