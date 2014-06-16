import django.dispatch
from lessons.models import LessonHistory

view_lesson_signal = django.dispatch.Signal(providing_args=['user'])


def view_lesson(sender, user, **kwargs):
    """
    Receives Lesson object and creates CourseHistory object for logged User.
    """
    if user.is_authenticated():
        LessonHistory.objects.create(lesson=sender, user=user)

view_lesson_signal.connect(view_lesson)
