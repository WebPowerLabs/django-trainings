import factory
import random
import string
from courses.models import Course, CourseFavourite, CourseHistory
from django.conf import settings
from profiles.models import InstructorProfile
from packages.models import Package, PackagePurchase
from lessons.models import Lesson


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
    name = factory.LazyAttribute(lambda t: random_string())
    order = 0


class CourseFavouriteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CourseFavourite


class CourseHistoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CourseHistory


class LessonFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda t: random_string())
    FACTORY_FOR = Lesson


class PackageFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda t: random_string())
    FACTORY_FOR = Package


class PackagePurchaseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = PackagePurchase
