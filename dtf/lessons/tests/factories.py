import factory
import random
import string
from lessons.models import Lesson, LessonFavourite, LessonHistory
from courses.models import Course
from tags.models import Tag
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
    # fields
    name = factory.LazyAttribute(lambda t: random_string())
    order = 0


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


class LessonFavouriteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = LessonFavourite


class LessonHistoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = LessonHistory
