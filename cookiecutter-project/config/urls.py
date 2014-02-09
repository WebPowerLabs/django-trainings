# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^d2f-community/$',
        TemplateView.as_view(template_name='pages/d2f-community.html'),
        name="d2f-community"),
    url(r'^courage-to-soar/$',
        TemplateView.as_view(template_name='pages/courage-to-soar.html'),
        name="courage-to-soar"),
    url(r'^accelerate-your-destiny/$',
        TemplateView.as_view(template_name='pages/accelerate-your-destiny.html'),
        name="accelerate-your-destiny"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
