# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from users.views import EmailVerificationSentView, LoginCustomView
from dtf_comments.views import CommentDeleteView
from courses import settings as trainings_settings

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r"^accounts/login/$", LoginCustomView.as_view(), name="account_login"),
    url(r'^accounts/confirm-email/$', EmailVerificationSentView.as_view(),
                                      name='account_email_verification_sent'),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here
    url(r'^blog/', include("blog.urls", namespace="blog")),
    url(r'^files/', include('nufiles.urls', namespace="nufiles")),
    url(r'^groups/', include('facebook_groups.urls',
                                                 namespace="facebook_groups")),
    url(r'^{}s/'.format(trainings_settings.COURSE_NAME.lower()), include('courses.urls', namespace="courses")),
    url(r'^{}s/'.format(trainings_settings.LESSON_NAME.lower()), include('lessons.urls', namespace="lessons")),
    url(r'^{}s/'.format(trainings_settings.RESOURCE_NAME.lower()), include('resources.urls', namespace="resources")),
    url(r'^tags/', include('tags.urls', namespace="tags")),
    url(r'^profiles/', include('profiles.urls', namespace="profiles")),
    url(r'^features/', include('features.urls', namespace="features")),
    url(r'^dtf_comments/', include('dtf_comments.urls',
                                   namespace="dtf_comments")),
    url(r'^comments/delete/(?P<comment_id>\d+)/$', CommentDeleteView.as_view(),
                                                    name='comments-delete'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^packages/', include('packages.urls', namespace="packages")),
    url(r'^journals/', include('journals.urls', namespace="journals")),
    url(r'^affiliates/', include('affiliates.urls', namespace="affiliates")),
    url(r'^etfar/', include('etfars.urls', namespace='etfars')),
    url(r'^', include('pages.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
