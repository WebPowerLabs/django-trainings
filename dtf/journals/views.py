from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Journal, JournalEntry

@login_required
def journal_entries_list(request):
    user = request.user
    journal = Journal.objects.get_or_create(author=user)[0]
    entries = JournalEntry.objects.filter(journal=journal.id)

    paginator = Paginator(entries, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    context = {
        'journal': journal,
        'entries': entries
    }
    if request.method == 'POST':
        new_entry_data = request.POST.copy()
        next = new_entry_data.get('next', None)
        if next:
            del new_entry_data['next']
        else:
            next = reverse_lazy("journals:entries")
        
        del new_entry_data[u'csrfmiddlewaretoken']
        JournalEntry.objects.create(journal=journal, 
                                    data=new_entry_data.dict())

        return HttpResponseRedirect(next)

    return render_to_response("journals/entries.html", context, 
                              context_instance=RequestContext(request))

