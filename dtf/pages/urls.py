from django.conf.urls import patterns, url
from .views import PageView, HMHPageView


urlpatterns = patterns('pages.views',
    url(r'^$',
        PageView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        PageView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^d2f-community/$',
        PageView.as_view(template_name='pages/d2f-community.html'),
        name="d2f-community"),
    url(r'^courage-to-soar/$',
        PageView.as_view(template_name='pages/courage-to-soar.html'),
        name="courage-to-soar"),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^search/$', 'search', name="search"),
    )
