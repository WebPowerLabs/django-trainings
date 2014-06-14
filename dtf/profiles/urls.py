from django.contrib.auth.decorators import login_required

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from profiles import views

urlpatterns = patterns('',
    url('^(?P<model_name>lesson|course)/(?P<pk>[-\w]+)$',
        login_required(views.FavouriteAddView.as_view()),
        name='add_favourite'))
