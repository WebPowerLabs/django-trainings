from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.http.response import HttpResponseRedirect

from lessons.models import Lesson
from utils.views import CreateFormBaseView

from .forms import ResourceCreateFrom
from .models import Resource


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

class ResourceAddView(CreateFormBaseView):
    model = Resource
    template_name = 'resources/resource_create.html'
    form_class = ResourceCreateFrom

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lesson = Lesson.objects.get(slug=self.kwargs['slug'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
