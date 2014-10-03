from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import InfusionsoftProfile, UserProfile, UserPrivateProfile
from .forms import UserProfileForm, UserPrivateProfileForm


@login_required
def update_infusionsoft_tags(request):
    '''
    updates users tags with infusionsofts
    '''
    redirect = request.GET.get('next') if request.GET.get('next') else reverse_lazy("users:redirect")

    profile = InfusionsoftProfile.objects.get_or_create(user=request.user)[0]
    profile.update_tags()

    return HttpResponseRedirect(redirect)

@login_required
def update_user_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    form = UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse_lazy("users:detail", 
                kwargs={"pk": request.user.pk}))
    context = {'form': form}
    return render_to_response("profiles/edit.html", context, 
        context_instance=RequestContext(request))


@login_required
def update_user_private_profile(request):
    user_profile = UserPrivateProfile.objects.get_or_create(user=request.user)[0]
    form = UserPrivateProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = UserPrivateProfileForm(request.POST, instance=user_profile)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse_lazy("users:detail", 
                kwargs={"pk": request.user.pk}))
    context = {'form': form}
    return render_to_response("profiles/edit.html", context, 
        context_instance=RequestContext(request))

