import factory
import random
import string
from resources.models import Resource


def random_string(length=8):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class ResourceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Resource
    # fields
    name = factory.LazyAttribute(lambda t: random_string())