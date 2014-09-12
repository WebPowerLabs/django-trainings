from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.http.response import HttpResponseRedirect

from lessons.models import Lesson
from utils.views import (CreateFormBaseView, PermissionMixin,
                            AjaxResponsePermissionMixin)

from .forms import ResourceCreateFrom
from .models import Resource
from braces.views._ajax import JSONResponseMixin
from django.views.generic.base import View
import json
from utils.decorators import (can_edit_content, instructor_member_required,
                              purchase_or_instructor_member_required)
from django.contrib.admin.views.decorators import staff_member_required


class ResourceListView(PermissionMixin, CreateFormBaseView):
    model = Resource
    queryset = Resource.objects.all()
    success_url = reverse_lazy('resources:list')
#     form_class = ResourceCreateFrom
    decorators = {'POST': staff_member_required,
                  'GET': instructor_member_required}

    def get_queryset(self):
        return Resource.objects.get_list(self.request.user)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.owner = self.request.user
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())


class ResourceDeleteView(PermissionMixin, DeleteView):
    model = Resource
    success_url = reverse_lazy('resources:list')
    decorators = {'GET': can_edit_content(Resource),
                  'POST': can_edit_content(Resource)}


class ResourceDetailView(PermissionMixin, UpdateView):
    model = Resource
    template_name = 'resources/detail.html'
    form_class = ResourceCreateFrom
    decorators = {'POST': can_edit_content(Resource),
                  'GET': purchase_or_instructor_member_required(Resource)}

    def get_queryset(self):
        return Resource.objects.get_list(self.request.user)

    def get_success_url(self):
        return reverse('resources:detail', kwargs={'slug': self.kwargs['slug']
                                                   })


class ResourceAddView(PermissionMixin, CreateFormBaseView):
    decorators = {'GET': can_edit_content(Lesson),
                  'POST': can_edit_content(Lesson)}
    model = Resource
    template_name = 'resources/resource_create.html'
    form_class = ResourceCreateFrom

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        initial = super(ResourceAddView, self).get_initial()
        initial = initial.copy()
        initial['type'] = self.request.GET.get('type', None)
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lesson = Lesson.objects.get(slug=self.kwargs['slug'])
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ResourceOrderView(AjaxResponsePermissionMixin, JSONResponseMixin, View):
    decorators = {'POST': can_edit_content(Lesson)}

    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        lesson = Lesson.objects.get(slug=self.kwargs['slug'])
        lesson.set_resource_order(data.get('new_order', None))
        return self.render_json_response({'success': True})
