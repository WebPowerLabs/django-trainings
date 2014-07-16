from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import InfusionsoftProfile



@login_required
def update_infusionsoft_tags(request):
    '''
    updates users tags with infusionsofts
    '''
    redirect = request.GET.get('next') if request.GET.get('next') else reverse_lazy("packages:purchases")

    profile = InfusionsoftProfile.objects.get_or_create(user=request.user)[0]
    profile.update_tags()

    return HttpResponseRedirect(redirect)