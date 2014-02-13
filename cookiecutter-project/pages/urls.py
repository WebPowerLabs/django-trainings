from django.conf.urls import patterns, url
from .views import PageView


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
    url(r'^accelerate-your-destiny/$',
        PageView.as_view(template_name='pages/accelerate-your-destiny.html'),
        name="accelerate-your-destiny"),
    url(r'^free-product/$',
        PageView.as_view(template_name='pages/free-product.html'),
        name="free-product"),
    url(r'^blog/$',
        PageView.as_view(template_name='pages/blog.html'),
        name="blog"),
    url(r'^blog-single/$',
        PageView.as_view(template_name='pages/blog-single.html'),
        name="blog-single"),
    url(r'^contact/$', 'contact', name='contact'),
    )