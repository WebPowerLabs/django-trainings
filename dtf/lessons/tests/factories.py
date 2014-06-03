import factory
import random
import string
from lessons.models import Lesson
from courses.models import Course
from tags.models import Tag


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class CourseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Course
    # fields
    name = factory.LazyAttribute(lambda t: random_string())


class TagFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Tag
    # fields
    name = factory.LazyAttribute(lambda t: random_string())


class LessonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Lesson
    # fields
    course = factory.SubFactory(CourseFactory)
    name = factory.LazyAttribute(lambda t: random_string())

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
