from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from utils.views import CreateFormBaseView, PermissionMixin
from tags.forms import TagCreateFrom
from tags.models import Tag
from utils.decorators import instructor_member_required


class TagListView(PermissionMixin, CreateFormBaseView):
    decorators = {'GET': instructor_member_required,
                  'POST': instructor_member_required}
    model = Tag
    queryset = Tag.objects.all()
    success_url = reverse_lazy('tags:list')
    form_class = TagCreateFrom


class TagDetailView(PermissionMixin, UpdateView):
    decorators = {'GET': instructor_member_required,
                  'POST': instructor_member_required}
    model = Tag
    template_name = 'tags/detail.html'
    form_class = TagCreateFrom

    def get_success_url(self):
        return reverse('tags:detail', kwargs={'pk': self.kwargs['pk']})


class TagDeleteView(PermissionMixin, DeleteView):
    decorators = {'GET': instructor_member_required,
                  'POST': instructor_member_required}
    model = Tag
    success_url = reverse_lazy('tags:list')
