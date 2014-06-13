from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from courses.models import Course
from django.views.generic import DeleteView
from courses.forms import CourseCreateFrom
from utils.views import CreateFormBaseView, PermissionMixin
from braces.views._ajax import AjaxResponseMixin, JSONResponseMixin
from django.views.generic.base import View
import json
from profiles.models import History


class CourseListView(PermissionMixin, CreateFormBaseView):
    model = Course
    success_url = reverse_lazy('courses:list')
    form_class = CourseCreateFrom
    decorators = {'POST': staff_member_required}

    def get_queryset(self):
        return Course.objects.get_list(self.request.user)


class CourseDetailView(PermissionMixin, UpdateView):
    model = Course
    template_name = 'courses/course_detail.html'
    form_class = CourseCreateFrom
    decorators = {'POST': staff_member_required}

    def get_queryset(self):
        return Course.objects.get_list(self.request.user)

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        context['lesson_list'] = course.lesson_set.get_list(self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        history = History(content_object=self.get_object(),
                          user=self.request.user)
        history.save()
        return UpdateView.get(self, request, *args, **kwargs)


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')


class CourseOrderView(AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        Course.objects.set_order(data.get('new_order', None))
        return self.render_json_response({'success': True})
