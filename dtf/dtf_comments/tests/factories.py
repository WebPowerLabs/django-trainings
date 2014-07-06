import factory
import random
import string
from factory.declarations import SubFactory
from courses.models import Content
from django.conf import settings
from facebook_groups.models import FacebookGroup


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = settings.AUTH_USER_MODEL
    first_name = factory.Sequence(lambda n: "First%s" % n)
    last_name = factory.Sequence(lambda n: "Last%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    is_staff = True


class ContentFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Content
    name = factory.LazyAttribute(lambda t: random_string())


class FacebookGroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = FacebookGroup
    name = factory.LazyAttribute(lambda t: random_string())
    fb_uid = 1
    owner = SubFactory(UserFactory)