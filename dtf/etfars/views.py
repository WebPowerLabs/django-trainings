from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Etfar
from .forms import EtfarForm


def etfar_tool_form_prep():
    form = EtfarForm()
    # remove submit button
    form.helper.layout.pop(5)
    form_clone = EtfarForm()
    # remove submit button
    form_clone.helper.layout.pop(5)
    # hide the clone
    form_clone.helper.form_class = "{} {}".format("hidden",
                                               form_clone.helper.form_class)
    form_clone.helper.form_id = "etfar_tool_clone"
    # remove the event field for new clones
    del form_clone.fields["event"]
    new_prefix = "<span class='new'>New </span>"
    for fieldname in form_clone.fields:
        form_clone.fields[fieldname].label = "{}{}".format(new_prefix,
                                                            form_clone.fields[
                                                             fieldname].label)

    return form, form_clone


@login_required
def etfar_tool(request):
    form, form_clone = etfar_tool_form_prep()
    etfars = Etfar.objects.filter(owner=request.user, active=True)
    context = {
        'etfar_form': form,
        'etfar_form_clone': form_clone,
        'etfars': etfars,
    }
    if request.method == 'POST':
        form = EtfarForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            #return HttpResponseRedirect(reverse_lazy('users:detail', 
            #                            kwargs={'pk': user.pk}))
            return HttpResponseRedirect(reverse_lazy('etfars:tool'))
    return render_to_response("etfars/tool.html", context, 
                              context_instance=RequestContext(request))