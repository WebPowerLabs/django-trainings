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
from .forms import FBGroupFeedForm, FBGroupCreateForm


@login_required
def fb_group_list(request):
    fb_groups = FacebookGroup.objects.all()
    context = {
        "facebook_groups": fb_groups,
    }
    return render_to_response('facebook_groups/list.html',
        context,
        context_instance = RequestContext(request))


@login_required
def sync_fb_data(request, fb_uid):
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    fb_group.save_fb_profile_data(request.user)
    return HttpResponseRedirect(reverse_lazy("facebook_groups:feed", kwargs={"fb_uid" : fb_group.fb_uid}))


@login_required
def fb_group_feed(request, fb_uid):
    fb_groups = FacebookGroup.objects.all()
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    feed = fb_group.get_fb_feed(request.user)

    context = {
        "facebook_groups": fb_groups,
        "facebook_group": fb_group,
        "feed" : feed,
    }
    return render_to_response('facebook_groups/feed.html',
        context,
        context_instance = RequestContext(request))

@login_required
def fb_group_feed_post(request, fb_uid):
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    form = FBGroupFeedForm()
    if request.method == 'POST':
        message = request.POST.get('message')
        fb_post = fb_group.post_fb_feed(request.user, message)
        return HttpResponseRedirect(reverse_lazy("facebook_groups:feed", kwargs={"fb_uid" : fb_group.fb_uid}))

    fb_groups = FacebookGroup.objects.all()
    context = {
        'facebook_groups': fb_groups,
        'facebook_group': fb_group,
        'form': form
    }
    return render_to_response('facebook_groups/post.html',
        context,
        context_instance = RequestContext(request))

@login_required
def fb_group_create(request):
    form = FBGroupCreateForm()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        privacy = request.POST.get('privacy')
        user = request.user
        fb_group = FacebookGroup.objects.fb_create(user=request.user.id, 
            name=name, description=description, privacy=privacy)
        return HttpResponseRedirect(reverse_lazy("facebook_groups:sync", kwargs={"fb_uid" : fb_group.fb_uid}))

    fb_groups = FacebookGroup.objects.all()
    context = {
        'facebook_groups': fb_groups,
        'form': form
    }
    return render_to_response('facebook_groups/add.html',
        context,
        context_instance = RequestContext(request))
