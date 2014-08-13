try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('profiles.views',
	url(r"^infusionsoft/update_tags/$", "update_infusionsoft_tags", name="infusionsoft_update_tags"),
	url(r"^user/update/$", "update_user_profile", name="update_user_profile")
	)