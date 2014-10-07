from django.conf.urls import patterns, url
from .views import PageView, HMHPageView, PublicCoursePageView


urlpatterns = patterns('pages.views',
    url(r'^public/sessions/(?P<slug>[-\w]+)/$',
        PublicCoursePageView.as_view(),
        name="public_sessions"),
    url(r'^$',
        PageView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        PageView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^search/$', 'search', name="search"),
    )
