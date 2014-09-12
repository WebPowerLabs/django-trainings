from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse_lazy

from .models import Journal, JournalEntry, JournalQuestion


def journal_entries_list(request):
    user = request.user
    journal = Journal.objects.get(author=user)
    entries = JournalEntry.objects.filter(journal=journal)

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
        del new_entry_data[u'csrfmiddlewaretoken']
        JournalEntry.objects.create(journal=journal, 
                                    data=new_entry_data.dict())
        return HttpResponseRedirect(reverse_lazy("journals:entries"))

    return render_to_response("journals/entries.html", context, 
                              context_instance=RequestContext(request))

