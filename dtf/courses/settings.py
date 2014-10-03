from django.conf import settings

COURSE_NAME = getattr(settings, 'COURSE_NAME', "Course")
LESSON_NAME = getattr(settings, 'LESSON_NAME', "Lesson")
RESOURCE_NAME = getattr(settings, 'RESOURCE_NAME', "Resource")
HOMEWORK_NAME = getattr(settings, 'HOMEWORK_NAME', "Homework")

