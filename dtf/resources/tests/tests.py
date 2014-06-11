from django_nose.testcases import FastFixtureTestCase
from django.contrib.auth.models import User
from resources.models import Resource
from resources.tests.factories import ResourceFactory


class ResourceManagerTest(FastFixtureTestCase):
    def setUp(self):
        self.course_pub = ResourceFactory(published=True)
        self.course_not_pub = ResourceFactory(published=False)
        self.fake_staff_user = User(username="staff", is_staff=True)
        self.fake_user = User(username="user", is_staff=False)
    
    def test_get_list_user_is_staff(self):
        total_count = Resource.objects.all().count()
        current_count = Resource.objects.get_list(self.fake_staff_user).count()
        self.assertEqual(total_count, current_count)
   
    def test_get_list_user_is_not_staff(self):
        total_count = Resource.objects.published().count()
        current_count = Resource.objects.get_list(self.fake_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_no_user(self):
        total_count = Resource.objects.published().count()
        current_count = Resource.objects.get_list().count()
        self.assertEqual(total_count, current_count)
