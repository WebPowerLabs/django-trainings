import django.dispatch
from courses.models import CourseHistory

view_course_signal = django.dispatch.Signal(providing_args=['user'])


def view_course(sender, user, **kwargs):
    """
    Receives Course object and creates CourseHistory object for logged User.
    """
    if user.is_authenticated():
        CourseHistory.objects.create(course=sender, user=user)

view_course_signal.connect(view_course)

