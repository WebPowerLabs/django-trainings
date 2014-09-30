from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Etfar
from .forms import EtfarForm


@login_required
def etfar_tool(request):
    user = request.user
    form = EtfarForm

    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = EtfarForm(request.POST)
        if form.is_valid():
            form.owner = user
            form.save()
            return HttpResponseRedirect(reverse_lazy('users:detail', 
                                        kwargs={'pk': user.pk}))
    return render_to_response("etfars/tool.html", context, 
                              context_instance=RequestContext(request))