from django.views.generic.edit import DeleteView, UpdateView
from lessons.models import Lesson, LessonFavourite, LessonHistory
from django.core.urlresolvers import reverse_lazy, reverse
from lessons.forms import LessonCreateFrom
from lessons.filters import LessonFilter
from django_filters.views import FilterView
from tags.models import Tag
from courses.models import Course
from utils.views import (CreateFormBaseView, PermissionMixin,
                            AjaxResponsePermissionMixin)
from django.http.response import HttpResponseRedirect
from braces.views._ajax import JSONResponseMixin
from django.views.generic.base import View
import json
from lessons.signals import view_lesson_signal
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from utils.decorators import can_edit_content


class LessonDetailView(PermissionMixin, UpdateView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    form_class = LessonCreateFrom
    decorators = {'GET': login_required,
                  'POST': can_edit_content(Lesson)}

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
        if self.request.user.is_authenticated():
            try:
                context['in_favourites'] = LessonFavourite.objects.get(
                                                        lesson=self.object,
                                                        user=self.request.user)
            except LessonFavourite.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'slug': self.kwargs['slug']})

    def get(self, request, *args, **kwargs):
        view_lesson_signal.send(sender=self.get_object(),
                                user=self.request.user)
        return UpdateView.get(self, request, *args, **kwargs)


class LessonListView(PermissionMixin, FilterView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    filterset_class = LessonFilter
    queryset = Lesson.objects.select_related('course')
    decorators = {'GET': login_required}

    def get_queryset(self):
        return Lesson.objects.get_list(self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['course_list'] = Course.objects.get_list(self.request.user)
        return context


class LessonAddView(PermissionMixin, CreateFormBaseView):
    model = Lesson
    template_name = 'lessons/lesson_create.html'
    form_class = LessonCreateFrom
    decorators = {'GET': can_edit_content(Course),
                  'POST': can_edit_content(Course)}

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.course = Course.objects.get(slug=self.kwargs['slug'])
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonDeleteView(PermissionMixin, DeleteView):
    model = Lesson
    success_url = reverse_lazy('lessons:list')
    decorators = {'GET': can_edit_content(Lesson),
                  'POST': can_edit_content(Lesson)}


class LessonOrderView(AjaxResponsePermissionMixin, JSONResponseMixin, View):
    decorators = {'POST': can_edit_content(Course)}

    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        course = Course.objects.get(slug=self.kwargs['slug'])
        course.set_lesson_order(data.get('new_order', None))
        return self.render_json_response({'success': True})


class LessonFavouriteActionView(AjaxResponsePermissionMixin, JSONResponseMixin,
                                View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=self.kwargs['pk'])
        obj, created = LessonFavourite.objects.get_or_create(lesson=lesson,
                                                    user=self.request.user)
        if not created:
            obj.is_active = not obj.is_active
            obj.save()
        return self.render_json_response({'success': True,
                                          'is_active': obj.is_active})


class LessonFavouriteListView(PermissionMixin, ListView):
    model = LessonFavourite
    decorators = {'GET': login_required}

    def get_queryset(self):
        return self.request.user.lessonfavourite_set.active()


class LessonHistoryListView(PermissionMixin, ListView):
    model = LessonHistory
    decorators = {'GET': login_required}

    def get_queryset(self):
        return self.request.user.lessonhistory_set.active()


class LessonHistoryDeleteView(AjaxResponsePermissionMixin, JSONResponseMixin,
                              View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        obj = LessonHistory.objects.get(pk=self.kwargs['pk'])
        obj.is_active = False
        obj.save()
        return self.render_json_response({'success': True})