from django.views.generic.edit import DeleteView, UpdateView
from lessons.models import Lesson
from django.core.urlresolvers import reverse_lazy, reverse
from lessons.forms import LessonCreateFrom
from lessons.filters import LessonFilter
from django_filters.views import FilterView
from tags.models import Tag
from courses.models import Course
from utils.views import CreateFormBaseView
from django.http.response import HttpResponseRedirect


class LessonDetailView(UpdateView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    form_class = LessonCreateFrom

    def get_context_data(self, **kwargs):
        tag_id = self.request.GET.get('tags', None)
        course_id = self.request.GET.get('course', None)
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['next_url'] = Lesson.objects.get_next_url(self.object, tag_id,
                                                          course_id)
        context['prev_url'] = Lesson.objects.get_prev_url(self.object, tag_id,
                                                          course_id)
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lessons:list')


class LessonListView(FilterView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    filterset_class = LessonFilter
    queryset = Lesson.objects.select_related('course')

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['course_list'] = Course.objects.all()
        return context


class LessonAddView(CreateFormBaseView):
    model = Lesson
    template_name = 'lessons/lesson_create.html'
    form_class = LessonCreateFrom

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.course = Course.objects.get(slug=self.kwargs['slug'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
