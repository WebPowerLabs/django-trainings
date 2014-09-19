from courses import settings


def trainings_names(request):
    return {
        'trainings': {
            'course_name': settings.COURSE_NAME,
            'lesson_name': settings.LESSON_NAME,
            'homework_name': settings.HOMEWORK_NAME,
            'resource_name': settings.RESOURCE_NAME
        }
    }