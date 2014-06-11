import factory
import random
import string
from courses.models import Course


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class CourseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Course
    # fields
    name = factory.LazyAttribute(lambda t: random_string())