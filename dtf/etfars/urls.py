try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('etfars.views',
                       url(r'^tool/$', 'etfar_tool', name='tool'),
                       )