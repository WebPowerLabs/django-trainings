from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from courses.models import Course
from django.views.generic import DeleteView
from courses.forms import CourseCreateFrom
from utils.views import CreateFormBaseView


class CourseListView(CreateFormBaseView):
    model = Course
    queryset = Course.objects.published()
    success_url = reverse_lazy('courses:list')
    form_class = CourseCreateFrom


class CourseDetailView(UpdateView):
    model = Course
    template_name = 'courses/course_detail.html'
    form_class = CourseCreateFrom

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs['slug']})


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')
