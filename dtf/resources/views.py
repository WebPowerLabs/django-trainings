from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.http.response import HttpResponseRedirect

from lessons.models import Lesson
from utils.views import CreateFormBaseView, PermissionMixin

from .forms import ResourceCreateFrom
from .models import Resource
from braces.views._ajax import AjaxResponseMixin, JSONResponseMixin
from django.views.generic.base import View
import json
from django.contrib.auth.decorators import login_required
from utils.decorators import instructor_member_required, can_edit_content


class ResourceListView(PermissionMixin, CreateFormBaseView):
    model = Resource
    queryset = Resource.objects.all()
    success_url = reverse_lazy('resources:list')
    form_class = ResourceCreateFrom
    decorators = {'POST': instructor_member_required, 'GET': login_required}

    def get_queryset(self):
        return Resource.objects.get_list(self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ResourceDeleteView(DeleteView, PermissionMixin):
    model = Resource
    success_url = reverse_lazy('resources:list')
    decorators = {'GET': login_required,
                  'POST': [instructor_member_required,
                           can_edit_content(Resource)]}


class ResourceDetailView(PermissionMixin, UpdateView):
    model = Resource
    template_name = 'resources/detail.html'
    form_class = ResourceCreateFrom
    decorators = {'POST': [instructor_member_required,
                           can_edit_content(Resource)],
                  'GET': login_required}

    def get_queryset(self):
        return Resource.objects.get_list(self.request.user)

    def get_success_url(self):
        return reverse('resources:detail', kwargs={'slug': self.kwargs['slug']
                                                   })


class ResourceAddView(CreateFormBaseView, PermissionMixin):
    model = Resource
    template_name = 'resources/resource_create.html'
    form_class = ResourceCreateFrom
    decorators = {'GET': login_required,
                  'POST': [instructor_member_required,
                           can_edit_content(Lesson)]}

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lesson = Lesson.objects.get(slug=self.kwargs['slug'])
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ResourceOrderView(AjaxResponseMixin, JSONResponseMixin, View,
                        PermissionMixin):
    decorators = {'POST': [instructor_member_required,
                           can_edit_content(Lesson)]}

    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
        lesson.set_resource_order(data.get('new_order', None))
        return self.render_json_response({'success': True})
