try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('journals.views',
    url(r'^entries/$', 'journal_entries_list', name='entries'),
    )