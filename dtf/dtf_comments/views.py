from dtf_comments.models import DTFComment
from utils.views import (AjaxResponsePermissionMixin,
                         CreateFormBaseView)
from dtf_comments.forms import DTFCommentForm, DTFCommentShareForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.shortcuts import render
import dtf_comments
from facebook_groups.models import FacebookGroup


class DTFCommentShareView(
#                           FormView
#                         AjaxResponsePermissionMixin,
                        CreateFormBaseView
                          ):

    model = DTFComment
    success_url = reverse_lazy('courses:list')
    form_class = DTFCommentShareForm
    decorators = {'GET': login_required}
    template_name = 'includes/share_form.html'
#
# def c_share(request):
#     f = FacebookGroup.objects.all()[0]
#     form = DTFCommentForm(f)
#
#     return render(request, 'includes/share_form.html',
#                   {'form': form})
