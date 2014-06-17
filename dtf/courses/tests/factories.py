import factory
import random
import string
from courses.models import Course, CourseFavourite, CourseHistory
from django.conf import settings


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = settings.AUTH_USER_MODEL
    first_name = factory.Sequence(lambda n: "First%s" % n)
    last_name = factory.Sequence(lambda n: "Last%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    is_staff = True


class CourseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Course
    name = factory.LazyAttribute(lambda t: random_string())
    order = 0


class CourseFavouriteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CourseFavourite


class CourseHistoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CourseHistory
