from django.shortcuts import render_to_response, get_object_or_404
# from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy, reverse
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, InvalidPage, EmptyPage
import django_comments
from packages.models import Package
from profiles.models import InfusionsoftProfile

Comment = django_comments.get_model()

from utils.comments import latest_comments

from .models import FacebookGroup
from .forms import FBGroupFeedForm, FBGroupCreateForm


@login_required
def fb_group_list(request):
    '''
    lists all facebook groups. also includes the latest comments from all 
    content types
    '''
    fb_groups = FacebookGroup.objects.all()
    if request.GET.get('purchased', None):
        fb_groups = FacebookGroup.objects.purchased(request.user)
    feed = latest_comments(request)  # get latest comments
    paginator = Paginator(feed, 10)  # TODO: add settings var: paginate_by
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        feed = paginator.page(page)
    except (EmptyPage, InvalidPage):
        feed = paginator.page(paginator.num_pages)

    context = {
        "facebook_groups": fb_groups,
        "feed": feed,
    }
    return render_to_response('facebook_groups/list.html',
        context,
        context_instance=RequestContext(request))


@login_required
def sync_fb_data(request, fb_uid):
    '''
    updates facebook_group with facebook's information about the group
    '''
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    fb_group.save_fb_profile_data(request.user)
    return HttpResponseRedirect(reverse_lazy("facebook_groups:detail",
        kwargs={"fb_uid" : fb_group.fb_uid}))


@login_required
def fb_group_detail(request, fb_uid):
    '''
    view of facebook group without the facebook feed. instead django_comments 
    are used in the template
    '''
    fb_groups = FacebookGroup.objects.all()
    if request.GET.get('purchased', None):
        fb_groups = FacebookGroup.objects.purchased(request.user)
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    content_type_id = ContentType.objects.get_for_model(FacebookGroup)
    comments = Comment.objects.filter(content_type=content_type_id,
        object_pk=fb_group.pk, is_removed=False).order_by('-submit_date')
    if fb_group.pinned_comment:
        comments = comments.exclude(pk=fb_group.pinned_comment.pk)
    paginator = Paginator(comments, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        comments = paginator.page(page)
    except (EmptyPage, InvalidPage):
        comments = paginator.page(paginator.num_pages)

    context = {
        "facebook_groups": fb_groups,
        "facebook_group": fb_group,
        "comments": comments
    }
    packages = Package.objects.filter(groups=fb_group)
    profile = InfusionsoftProfile.objects.get_or_create(user=request.user)[0]
    profile.update_tags()
    purchased_groups = FacebookGroup.objects.purchased(request.user)
    if fb_group not in purchased_groups and not request.user.is_staff:
        if len(packages) > 1:
                return HttpResponseRedirect(reverse('packages:list_for_group',
                                                kwargs={'group_pk': fb_group.pk}))
        return HttpResponseRedirect(reverse('packages:detail',
                                            kwargs={'pk': packages[0].pk}))

    return render_to_response('facebook_groups/detail.html',
                                context,
                                context_instance=RequestContext(request))


@login_required
def pin_comment(request, fb_uid, comment_id):
    '''
    saves a comment as the pinned_comment field of a facebook_group
    '''
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    fb_group.pin_comment(comment_id)
    return HttpResponseRedirect(reverse_lazy("facebook_groups:detail",
        kwargs={"fb_uid" : fb_uid}))


@login_required
def unpin_comment(request, fb_uid):
    '''
    removes the facebook_group's pinned_comment
    '''
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    fb_group.unpin_comment()
    return HttpResponseRedirect(reverse_lazy("facebook_groups:detail",
        kwargs={"fb_uid" : fb_uid}))


@login_required
def fb_group_feed(request, fb_uid):
    '''
    fetches the facebook_group's feed from the fb api and returns it as a 
    dictionary
    '''
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
        context_instance=RequestContext(request))


@login_required
def fb_group_feed_post(request, fb_uid):
    '''
    posts to the facebook_group's fb feed via the fb api
    '''
    fb_group = get_object_or_404(FacebookGroup, fb_uid=fb_uid)
    form = FBGroupFeedForm()
    if request.method == 'POST':
        message = request.POST.get('message')
        fb_group.post_fb_feed(request.user, message)
        return HttpResponseRedirect(reverse_lazy("facebook_groups:feed",
            kwargs={"fb_uid" : fb_group.fb_uid}))

    fb_groups = FacebookGroup.objects.all()
    context = {
        'facebook_groups': fb_groups,
        'facebook_group': fb_group,
        'form': form
    }
    return render_to_response('facebook_groups/post.html',
        context,
        context_instance=RequestContext(request))


@login_required
def fb_group_create(request):
    '''
    creates a new facebook_group on the local database as well as on facebook
    redirects to sync view instead of syncing here
    '''
    form = FBGroupCreateForm()
    if request.method == 'POST':
        form = form(request)
        name = request.POST.get('name')
        description = request.POST.get('description')
        privacy = request.POST.get('privacy')
        fb_group = FacebookGroup.objects.fb_create(user=request.user.id,
            name=name, description=description, privacy=privacy)
        # sync with fb data
        fb_group.save_fb_profile_data(request.user)
        return HttpResponseRedirect(reverse_lazy("facebook_groups:detail",
            kwargs={"fb_uid" : fb_group.fb_uid}))
    context = {
        'form': form
    }
    return render_to_response('facebook_groups/add.html',
        context,
        context_instance=RequestContext(request))


@login_required
def fb_group_edit(request, fb_uid):
    '''
    edits facebook_group on the local database as well as on facebook
    redirects to sync view instead of syncing here
    '''
    fb_group = FacebookGroup.objects.get(fb_uid=fb_uid)
    
    if request.method == 'POST':
        form = FBGroupCreateForm(request.POST, request.FILES, instance=fb_group)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse_lazy("facebook_groups:detail",
                kwargs={"fb_uid" : fb_group.fb_uid}))
    form = FBGroupCreateForm(instance=fb_group)
    context = {
        'form': form
    }
    return render_to_response('facebook_groups/add.html',
        context,
        context_instance=RequestContext(request))
