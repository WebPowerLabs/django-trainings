import requests, json

from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic.base import TemplateView


from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view

from .models import FacebookGroup


@login_required
def sync_fb_data(request, fb_uid):
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    fb_group.save_fb_profile_data(request.user)
    return HttpResponseRedirect(reverse_lazy("facebook_groups:feed", kwargs={"fb_uid" : fb_group.fb_uid}))


@login_required
def fb_group_feed(request, fb_uid):
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    if request.GET.get("page"):
        print request.GET.get("page")
        feed = requests.get(request.GET.get("page")).json()
    else:
        feed = fb_group.get_fb_feed(request.user)
    print feed
    context = {
        "facebook_group": fb_group,
        "feed" : feed,
    }
    return render_to_response('facebook_groups/feed.html',
        context,
        context_instance = RequestContext(request))