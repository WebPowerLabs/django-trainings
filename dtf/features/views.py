from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.db import models

from .forms import FeatureForm


def feature_create(request):
    '''
    
    '''
    form = FeatureForm()
    if request.method == 'POST':
        content_type = ''
        object_pk = ''
        comment = ''
        #fb_group = FacebookGroup.objects.fb_create(user=request.user.id, 
        #    name=name, description=description, privacy=privacy)
        return HttpResponseRedirect(reverse_lazy("features:redirect",
            args=[content_type, object_pk]))

    
    context = {
        'form': form,
    }
    return render_to_response('features/add.html',
        context,
        context_instance = RequestContext(request))


def feature_create_comment(request, object_pk=None, class_name=None):
    '''
    
    '''
    form = FeatureForm()
    print class_name.split(".models.", 1)
    #obj_model = models.get_model(class_name.split(".models.", 1))
    try:
        obj_model = models.get_model(*class_name.split(".models.", 1))
        print obj_model
    except TypeError:
        raise Http404
    obj = get_object_or_404(obj_model, pk=object_pk)
    if request.method == 'POST':
        content_type = ''
        object_pk = ''
        comment = ''
        #fb_group = FacebookGroup.objects.fb_create(user=request.user.id, 
        #    name=name, description=description, privacy=privacy)
        return HttpResponseRedirect(reverse_lazy("features:redirect",
            args=[content_type, object_pk]))

    
    context = {
        'form': form,
    }
    return render_to_response('features/add.html',
        context,
        context_instance = RequestContext(request))