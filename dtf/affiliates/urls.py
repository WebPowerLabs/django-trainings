try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from affiliates import views


urlpatterns = patterns('affiliates.views',
    url('^$', views.PartnerListView.as_view(), 
        name='partner_list'),
    url('^(?P<slug>[-\w]+)/$', views.PartnerDetailView.as_view(), 
        name='partner_detail'),
    )