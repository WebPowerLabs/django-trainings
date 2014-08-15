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
    url(r'^buy-d2f-community/$',
        PageView.as_view(template_name='pages/buy-d2f-community.html'),
        name="buy-community"),
    url(r'^become-a-leader/$',
        PageView.as_view(template_name='pages/become-a-leader.html'),
        name="become-leader"),
    url(r'^courage-to-soar/$',
        PageView.as_view(template_name='pages/courage-to-soar.html'),
        name="courage-to-soar"),
    url(r'^buy-courage-to-soar/$',
        PageView.as_view(template_name='pages/buy-courage-to-soar.html'),
        name="buy-cts"),
    url(r'^accelerate-your-destiny/$',
        PageView.as_view(template_name='pages/accelerate-your-destiny.html'),
        name="accelerate-your-destiny"),
    url(r'^buy-accelerate-your-destiny/$',
        PageView.as_view(template_name='pages/buy-accelerate-your-destiny.html'),
        name="buy-ayd"),
    url(r'^mentorship-moments/$',
        PageView.as_view(template_name='pages/mentorship-moments.html'),
        name="mentorship-moments"),
    url(r'^blog/$',
        PageView.as_view(template_name='pages/blog.html'),
        name="blog"),
    url(r'^blog-single/$',
        PageView.as_view(template_name='pages/blog-single.html'),
        name="blog-single"),
    url(r'^coming-soon/$',
        PageView.as_view(template_name='pages/coming-soon.html'),
        name="coming-soon"),
    url(r'^hmh_promo/$',
        PageView.as_view(template_name='pages/hmh_sell_page.html'),
        name="hmh-sell-1"),
    url(r'^hmh_video/$',
        PageView.as_view(template_name='pages/hmh_video.html'),
        name="hmh-video"),
    url(r'^terms-of-service/$',
        PageView.as_view(template_name='pages/terms-of-service.html'),
        name="terms-of-service"),
    url(r'^meet-the-founder/$',
        PageView.as_view(template_name='pages/meet_the_founder.html'),
        name="meet-the-founder"),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^search/$', 'search', name="search"),
    )
