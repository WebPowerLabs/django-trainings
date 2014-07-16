from django.shortcuts import get_object_or_404
#from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy
#from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import InfusionsoftProfile



@login_required
def update_infusionsoft_tags(request):
    '''
    '''
    redirect = request.GET.get('next') if request.GET.get('next') else reverse_lazy("users:redirect")

    profile = InfusionsoftProfile.objects.get_or_create(user=request.user)[0]
    profile.update_tags()
    print profile.tags.all()
        
    return HttpResponseRedirect(redirect)