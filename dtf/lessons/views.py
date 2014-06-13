from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import DeleteView, UpdateView
from lessons.models import Lesson
from django.core.urlresolvers import reverse_lazy, reverse
from lessons.forms import LessonCreateFrom
from lessons.filters import LessonFilter
from django_filters.views import FilterView
from tags.models import Tag
from courses.models import Course
from utils.views import CreateFormBaseView, PermissionMixin
from django.http.response import HttpResponseRedirect
from braces.views._ajax import AjaxResponseMixin, JSONResponseMixin
from django.views.generic.base import View
import json
from profiles.models import History


class LessonDetailView(PermissionMixin, UpdateView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    form_class = LessonCreateFrom
    decorators = {'POST': staff_member_required}

    def get_queryset(self):
        return Lesson.objects.get_list(self.request.user)

    def get_context_data(self, **kwargs):
        tag_id = self.request.GET.get('tags', None)
        course_id = self.request.GET.get('course', None)
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['resource_list'] = Lesson.get_resource(self.object,
                                                       self.request.user)
        context['homework_list'] = Lesson.get_homework(self.object,
                                                       self.request.user)
        context['next_url'] = Lesson.objects.get_next_url(self.object, tag_id,
                                                course_id, self.request.user)
        context['prev_url'] = Lesson.objects.get_prev_url(self.object, tag_id,
                                                course_id, self.request.user)
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})

    def get(self, request, *args, **kwargs):
        history = History(content_object=self.get_object(),
                          user=self.request.user)
        history.save()
        return UpdateView.get(self, request, *args, **kwargs)


class LessonListView(PermissionMixin, FilterView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    filterset_class = LessonFilter
    queryset = Lesson.objects.select_related('course')
    decorators = {'POST': staff_member_required}

    def get_queryset(self):
        return Lesson.objects.get_list(self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['course_list'] = Course.objects.get_list(self.request.user)
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


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy('lessons:list')


class LessonOrderView(AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        course.set_lesson_order(data.get('new_order', None))
        return self.render_json_response({'success': True})
