from functools import wraps
from profiles.models import InstructorProfile
from django.http.response import Http404, HttpResponseRedirect
from courses.models import Course, Content
from lessons.models import Lesson
from resources.models import Resource
from django.core.urlresolvers import reverse
from packages.models import Package
from profiles.models import InfusionsoftProfile
from django.shortcuts import get_object_or_404


def  purchase_or_instructor_member_required(model):
    """
    Decorator for views. Receives model of content. Returns view if there is no
    package associated with the content or user is a staff or instructor member
    or user has PackagePurchase. Redirects to content purchase page if not.
    """
    if model not in [Course, Lesson, Resource]:
        error_message = '{} should be one of the next models [Course, Lesson, Resource]'
        raise ValueError(error_message.format(model))

    def wrapper(view_func):
        @wraps(view_func)
        def check(request, *args, **kwargs):
            user = request.user
            profile = InfusionsoftProfile.objects.get_or_create(user=user)[0]
            profile.update_tags()
            slug = kwargs.get('slug', None)
            content = get_object_or_404(Content, slug=slug)
            purchased_list = model.objects.purchased(user)
            packages = Package.objects.get_for_content(content)
            if user.is_authenticated() and user.is_active:
                try:
                    instructor = user.instructorprofile
                except InstructorProfile.DoesNotExist:
                    instructor = False
                if content in purchased_list or user.is_staff or instructor:
                    return view_func(request, *args, **kwargs)
            # if multiple packages exist return a list of purchase options
            if len(packages) > 1:
                return HttpResponseRedirect(
                                        reverse('packages:list_for_content',
                                    kwargs={'content_pk': content.lesson.pk}))
            # if only one exists return the package
            return HttpResponseRedirect(reverse('packages:detail',
                                                kwargs={'pk': packages[0].pk}))
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
