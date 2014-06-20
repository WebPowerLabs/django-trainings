from functools import wraps
from profiles.models import InstructorProfile
from django.http.response import Http404
from courses.models import Course
from lessons.models import Lesson
from resources.models import Resource
from django.shortcuts import get_object_or_404


def instructor_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff 
    or instructor member. Raises 404 if not.
    """
    @wraps(view_func)
    def check(request, *args, **kwargs):
        try:
            instructor = request.user.instructorprofile
        except InstructorProfile.DoesNotExist:
            instructor = False
        if request.user.is_active and (request.user.is_staff or instructor):
            return view_func(request, *args, **kwargs)
        raise Http404
    return check


def can_edit_content(model):
    """
    Decorator for views that checks that the user is owner of content object.
    Raises 404 if not.
    """
    if model not in [Course, Lesson, Resource]:
        raise ValueError('{} should be one of the models [Course, Lesson, Resource]'.format(model))

    def wrapper(view_func):
        @wraps(view_func)
        def check(request, *args, **kwargs):
            slug = kwargs.get('slug', None)
            content = model.objects.get(slug=slug)
#             parent = content.owner
#             if model == Lesson:
#                 parent = model.course.owner
#             elif model == Resource:
#                 parent = model.lesson.owner
            if content.owner == request.user:
                return view_func(request, *args, **kwargs)
            raise Http404
        return check
    return wrapper



