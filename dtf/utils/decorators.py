from functools import wraps
from profiles.models import InstructorProfile
from django.http.response import Http404, HttpResponseRedirect
from courses.models import Course
from lessons.models import Lesson
from resources.models import Resource
from django.core.urlresolvers import reverse
from packages.models import Package
from django.db.models import Q


def  purchase_or_instructor_member_required(model):
    """
    Decorator for views. Receives model of content. Returns view if there is no
    package associated with the content or user is a staff or instructor member
    or user has PackagePurchase. Redirects to content purchase page if not.
    """
    if model not in [Course, Lesson, Resource]:
        raise ValueError('{} should be one of the next models [Course, Lesson, Resource]'.format(model))

    def wrapper(view_func):
        @wraps(view_func)
        def check(request, *args, **kwargs):
            user = request.user
            slug = kwargs.get('slug', None)
            if user.is_authenticated() and user.is_active:
                content = model.objects.get(slug=slug)
                packages = Package.objects.filter(Q(courses=content) |
                                                  Q(lessons=content) |
                                                  Q(courses=content.course))
                try:
                    instructor = user.instructorprofile
                except InstructorProfile.DoesNotExist:
                    instructor = False
                if not packages or content in model.objects.purchased(user) or user.is_staff or instructor:
                    return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('packages:list_to_content',
                                            kwargs={'content_pk': content.pk}))
        return check
    return wrapper


def instructor_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    or instructor member. Raises 404 if not.
    """
    @wraps(view_func)
    def check(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated() and user.is_active:
            try:
                instructor = user.instructorprofile
            except InstructorProfile.DoesNotExist:
                instructor = False
            if user.is_staff or instructor:
                return view_func(request, *args, **kwargs)
        raise Http404
    return check


def can_edit_content(model):
    """
    Decorator for views that checks that the user is staff or is owner
    of content object. Raises 404 if not.
    """
    if model not in [Course, Lesson, Resource]:
        raise ValueError('{} should be one of the next models [Course, Lesson, Resource]'.format(model))

    def wrapper(view_func):
        @wraps(view_func)
        def check(request, *args, **kwargs):
            user = request.user
            slug = kwargs.get('slug', None)
            content = model.objects.get(slug=slug)
            if user.is_authenticated() and user.is_active and (user.is_staff or content.owner == user):
                return view_func(request, *args, **kwargs)
            raise Http404
        return check
    return wrapper
