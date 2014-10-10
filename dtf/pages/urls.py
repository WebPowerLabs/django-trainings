from django.conf.urls import patterns, url
from .views import PageView, HMHPageView


urlpatterns = patterns('pages.views',
    url(r'^$',
        PageView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^search/$', 'search', name="search"),
    )
