from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from utils.views import CreateFormBaseView, PermissionMixin
from tags.forms import TagCreateFrom
from tags.models import Tag


class TagListView(PermissionMixin, CreateFormBaseView):
    model = Tag
    queryset = Tag.objects.all()
    success_url = reverse_lazy('tags:list')
    form_class = TagCreateFrom
    decorators = {'POST': staff_member_required}


class TagDetailView(PermissionMixin, UpdateView):
    model = Tag
    template_name = 'tags/detail.html'
    form_class = TagCreateFrom
    decorators = {'POST': staff_member_required}

    def get_success_url(self):
        return reverse('tags:detail', kwargs={'pk': self.kwargs['pk']})


class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('tags:list')