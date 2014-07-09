try:
    from django.conf.urls import url, patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import PackageListView, PackageDetailView

urlpatterns = patterns('package.views',
	url(r'^$', PackageListView.as_view(), name='list'),
	url(r'^(?P<pk>\d+)/$', PackageDetailView.as_view(), name='detail'),
	)