from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from courses.models import Course, CourseFavourite, CourseHistory
from django.views.generic import DeleteView
from courses.forms import CourseCreateFrom
from utils.views import (CreateFormBaseView, PermissionMixin,
                         AjaxResponsePermissionMixin)
from braces.views._ajax import JSONResponseMixin
from django.views.generic.base import View
from courses.signals import view_course_signal
import json
from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect
from utils.decorators import instructor_member_required, can_edit_content
from facebook_groups.models import FacebookGroup
from lessons.models import LessonComplete


class CourseListView(PermissionMixin, CreateFormBaseView):
    model = Course
    success_url = reverse_lazy('courses:list')
    form_class = CourseCreateFrom
    decorators = {'POST': instructor_member_required}

    def get_queryset(self):
        return Course.objects.get_list(self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CourseDetailView(PermissionMixin, UpdateView):
    model = Course
    template_name = 'courses/course_detail.html'
    form_class = CourseCreateFrom
    decorators = {'POST': can_edit_content(Course),
                  'GET': login_required}

    def get_queryset(self):
        return Course.objects.get_list(self.request.user)

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        context['lesson_list'] = course.lesson_set.get_list(self.request.user)
        context['fb_group_list'] = FacebookGroup.objects.purchased(
                                                           self.request.user)
        lesson_total = self.get_object().lesson_set.published().count()
        lesson_completed = LessonComplete.objects.filter(
                                               lesson__published=True,
                                               user=self.request.user,
                                               is_complete=True,
                                               lesson__course=self.get_object()
                                               ).count()
        try:
            context['course_completion'] = round(
                             float(lesson_completed) / lesson_total * 100, 2)
        except ZeroDivisionError:
            context['course_completion'] = 0

        if self.request.user.is_authenticated():
            try:
                context['is_favourite'] = CourseFavourite.objects.get(
                                                        course=self.object,
                                                        user=self.request.user
                                                        ).is_active
            except CourseFavourite.DoesNotExist:
                pass
        return context

    def get(self, request, *args, **kwargs):
        view_course_signal.send(sender=self.get_object(),
                                user=self.request.user)
        return UpdateView.get(self, request, *args, **kwargs)


class CourseDeleteView(PermissionMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')
    decorators = {'GET': can_edit_content(Course),
                  'POST': can_edit_content(Course)}


class CourseOrderView(AjaxResponsePermissionMixin, JSONResponseMixin, View):
    decorators = {'POST': staff_member_required}

    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.read())
        Course.objects.set_order(data.get('new_order', None))
        return self.render_json_response({'success': True})


class CourseFavouriteActionView(AjaxResponsePermissionMixin, JSONResponseMixin,
                                View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs['slug'])
        obj, created = CourseFavourite.objects.get_or_create(course=course,
                                                     user=self.request.user)
        if not created:
            obj.is_active = not obj.is_active
            obj.save()
        return self.render_json_response({'success': True,
                                          'is_active': obj.is_active})


class CourseFavouriteListView(PermissionMixin, ListView):
    model = CourseFavourite
    decorators = {'GET': login_required}

    def get_queryset(self):
        return CourseFavourite.objects.active(self.request.user)


class CourseHistoryListView(PermissionMixin, ListView):
    model = CourseHistory
    decorators = {'GET': login_required}

    def get_queryset(self):
        return CourseHistory.objects.active(self.request.user)


class CourseHistoryDeleteView(AjaxResponsePermissionMixin, JSONResponseMixin,
                              View):
    decorators = {'POST': login_required}

    def post_ajax(self, request, *args, **kwargs):
        obj = CourseHistory.objects.get(pk=self.kwargs['pk'])
        obj.is_active = False
        obj.save()
        return self.render_json_response({'success': True})
