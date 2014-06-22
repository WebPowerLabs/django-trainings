import factory
import random
import string
from django.conf import settings
from profiles.models import InstructorProfile
from resources.models import Resource
from lessons.models import Lesson
from courses.models import Course


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = settings.AUTH_USER_MODEL
    first_name = factory.Sequence(lambda n: "First%s" % n)
    last_name = factory.Sequence(lambda n: "Last%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    is_staff = True
    
class InstructorProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = InstructorProfile


class CourseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Course
    # fields
    name = factory.LazyAttribute(lambda t: random_string())
    order = 0
    owner = factory.SubFactory(UserFactory)


class LessonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Lesson
    # fields
    name = factory.LazyAttribute(lambda t: random_string())
    course = factory.SubFactory(CourseFactory)
    published = True


class ResourceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Resource
    # fields
    name = factory.LazyAttribute(lambda t: random_string())