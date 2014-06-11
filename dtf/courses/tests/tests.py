from django_nose.testcases import FastFixtureTestCase
from courses.models import Course
from courses.tests.factories import CourseFactory
from django.contrib.auth.models import User

class CourseManagerTest(FastFixtureTestCase):
    def setUp(self):
        self.course_pub = CourseFactory(published=True)
        self.course_not_pub = CourseFactory(published=False)
        self.fake_staff_user = User(username="staff", is_staff=True)
        self.fake_user = User(username="user", is_staff=False)
    
    def test_get_list_user_is_staff(self):
        total_count = Course.objects.all().count()
        current_count = Course.objects.get_list(self.fake_staff_user).count()
        self.assertEqual(total_count, current_count)
   
    def test_get_list_user_is_not_staff(self):
        total_count = Course.objects.published().count()
        current_count = Course.objects.get_list(self.fake_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_no_user(self):
        total_count = Course.objects.published().count()
        current_count = Course.objects.get_list().count()
        self.assertEqual(total_count, current_count)
