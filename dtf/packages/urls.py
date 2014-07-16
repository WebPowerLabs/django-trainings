try:
    from django.conf.urls import url, patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import PackageListView, PackageDetailView, PackagePurchaseListView, PackageListToContentView

urlpatterns = patterns('package.views',
	url(r'^$', PackageListView.as_view(), name='list'),
	url(r'^(?P<pk>\d+)/$', PackageDetailView.as_view(), name='detail'),
	url(r'^purchases/$', PackagePurchaseListView.as_view(), name='purchases'),
    url(r'^content/(?P<content_pk>[-\w]+)/$',
        PackageListToContentView.as_view(), name='list_to_content'),
	)
