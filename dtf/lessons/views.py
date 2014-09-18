from django.views.generic.edit import DeleteView, UpdateView
from lessons.models import (Lesson, LessonFavourite, LessonHistory,
                            LessonComplete)
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
from utils.decorators import (can_edit_content,
                              purchase_or_instructor_member_required)
from facebook_groups.models import FacebookGroup


class LessonDetailView(PermissionMixin, UpdateView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    form_class = LessonCreateFrom
    decorators = {'GET': purchase_or_instructor_member_required(Lesson),
                  'POST': can_edit_content(Lesson)}

    def get_context_data(self, **kwargs):
        lesson = self.object
        user = self.request.user
        tag_id = self.request.GET.get('tags', None)
        course_id = self.request.GET.get('course', None)
        purchased = self.request.GET.get('purchased', None)
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['resource_list'] = Lesson.get_resource(lesson, user)
        context['homework_list'] = Lesson.get_homework(lesson, user)
        context['can_start'] = lesson.can_start(user)
        context['current_lesson'] = Lesson.objects.get_current(user, 
                                                               lesson.course)
        context['next_url'] = Lesson.objects.get_next_url(lesson, tag_id,
                                                          course_id, purchased,
                                                          user)
        context['prev_url'] = Lesson.objects.get_prev_url(lesson, tag_id,
                                                          course_id, purchased,
                                                          user)
        context['fb_group_list'] = FacebookGroup.objects.purchased(user)
        try:
            context['is_favourite'] = LessonFavourite.objects.get(user=user,
                                                                  lesson=lesson
                                                                  ).is_active
        except LessonFavourite.DoesNotExist:
            pass
        try:
            context['is_complete'] = LessonComplete.objects.get(user=user,
                                                                lesson=lesson
                                                                ).is_complete
        except LessonComplete.DoesNotExist:
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
        if self.request.GET.get('purchased', None):
            return Lesson.objects.purchased(self.request.user
                                            ).order_by('-created')
        return Lesson.objects.get_list(self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['course_list'] = Course.objects.get_list(self.request.user)
        if self.request.GET.get('purchased', None):
            context['course_list'] = Course.objects.purchased(
                                                          self.request.user)
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
        form.save_m2m()
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
        lesson = Lesson.objects.get(slug=self.kwargs['slug'])
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
        return LessonFavourite.objects.active(self.request.user)


class LessonHistoryListView(PermissionMixin, ListView):
    model = LessonHistory
    decorators = {'GET': login_required}

    def get_queryset(self):
        return LessonHistory.objects.active(self.request.user)


class LessonHistoryDeleteView(AjaxResponsePermissionMixin, JSONResponseMixin,
                              View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        obj = LessonHistory.objects.get(pk=self.kwargs['pk'])
        obj.is_active = False
        obj.save()
        return self.render_json_response({'success': True})


class LessonCompleteActionView(AjaxResponsePermissionMixin, JSONResponseMixin,
                           View):
    decorators = {'POST': purchase_or_instructor_member_required(Lesson)}

    def post_ajax(self, request, *args, **kwargs):
        user = self.request.user
        lesson = Lesson.objects.get(slug=self.kwargs['slug'])
        obj, created = LessonComplete.objects.get_or_create(lesson=lesson,
                                                            user=user)
        if not created:
            obj.is_complete = not obj.is_complete
            obj.save()
        return self.render_json_response({'success': True,
                                          'is_active': obj.is_complete})
