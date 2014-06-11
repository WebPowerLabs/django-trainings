from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from courses.models import Course
from django.views.generic import DeleteView
from courses.forms import CourseCreateFrom
from utils.views import CreateFormBaseView, PermissionMixin


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


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')
