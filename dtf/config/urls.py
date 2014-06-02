# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here
    url(r'^blog/', include("blog.urls", namespace="blog")),
    url(r'^files/', include('nufiles.urls', namespace="nufiles")),
    url(r'^groups/', include('facebook_groups.urls',
                                                 namespace="facebook_groups")),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^lessons/', include('lessons.urls', namespace="lessons")),
    url(r'^resources/', include('resources.urls', namespace="resources")),
    url(r'^tags/', include('tags.urls', namespace="tags")),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^', include('pages.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
