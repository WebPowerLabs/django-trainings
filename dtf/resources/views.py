from resources.models import Resource
from utils.views import CreateFormBaseView
from django.core.urlresolvers import reverse_lazy, reverse
from resources.forms import ResourceCreateFrom
from django.views.generic.edit import DeleteView, UpdateView


class ResourceListView(CreateFormBaseView):
    model = Resource
    queryset = Resource.objects.all()
    success_url = reverse_lazy('resources:list')
    form_class = ResourceCreateFrom


class ResourceDeleteView(DeleteView):
    model = Resource
    success_url = reverse_lazy('resources:list')


class ResourceDetailView(UpdateView):
    model = Resource
    template_name = 'resources/detail.html'
    form_class = ResourceCreateFrom

    def get_success_url(self):
        return reverse('resources:detail', kwargs={
                                                  'slug': self.kwargs['slug']})
