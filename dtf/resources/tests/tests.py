from django_nose.testcases import FastFixtureTestCase
from resources.models import Resource
from resources.tests.factories import (ResourceFactory, LessonFactory,
                                       UserFactory, InstructorProfileFactory,
                                       PackageFactory, CourseFactory,
                                       PackagePurchaseFactory)
from django.test.client import Client
import json
from django.core.urlresolvers import reverse
from utils.tests import TestCaseBase


class ResourceManagerTest(TestCaseBase):
    def setUp(self):
        self.password = 'password'
        self.instructor = UserFactory(username='instructor', is_staff=False)
        self.instructor.set_password(self.password)
        self.instructor.save()
        self.user = UserFactory(username="user", is_staff=False)
        self.user.set_password(self.password)
        self.user.save()
        self.staff_user = UserFactory(username="staff", is_staff=True)
        self.staff_user.set_password(self.password)
        self.staff_user.save()

        self.instructor_profile = InstructorProfileFactory(
                                                       user=self.instructor)

        self.course = CourseFactory()
        self.lesson = LessonFactory(owner=self.user, course=self.course)
        self.lesson_purchased = LessonFactory(owner=self.user,
                                              course=self.course)
        self.lesson_not_purchased = LessonFactory(owner=self.user,
                                              course=self.course)

        self.res_pub = ResourceFactory(lesson=self.lesson_purchased,
                                       published=True,
                                       owner=self.user)
        self.res_not_pub = ResourceFactory(lesson=self.lesson, published=False,
                                           owner=self.user)
        self.res_not_purch = ResourceFactory(lesson=self.lesson_not_purchased,
                                             published=False,
                                             owner=self.user)
        self.package_one = PackageFactory()
        self.package_one.lessons.add(self.lesson_purchased)
        self.package_two = PackageFactory()
        self.package_two.lessons.add(self.lesson_not_purchased)
        self.package_purchased = PackagePurchaseFactory(user=self.user,
                                                    package=self.package_one,
                                                    status=1)

    def test_purchased(self):
        purchased = [self.res_pub, self.res_not_pub]
        res = Resource.objects.purchased(self.user)
        self.assertEqualQs(res, purchased)

    def test_get_list_user_had_insrtuctor_profile(self):
        total_count = Resource.objects.all().count()
        current_count = Resource.objects.get_list(self.instructor).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_user_is_staff(self):
        total_count = Resource.objects.all().count()
        current_count = Resource.objects.get_list(self.staff_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_user_is_not_staff(self):
        total_count = Resource.objects.published().count()
        current_count = Resource.objects.get_list(self.user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_no_user(self):
        total_count = Resource.objects.published().count()
        current_count = Resource.objects.get_list().count()
        self.assertEqual(total_count, current_count)


class ResourceViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.lesson = LessonFactory(owner=self.user)
        self.res_one = ResourceFactory(owner=self.user, lesson=self.lesson)
        self.res_two = ResourceFactory(owner=self.user, lesson=self.lesson)
        self.res_three = ResourceFactory(owner=self.user, lesson=self.lesson)

    def test_order_view(self):
        self.client.login(username=self.username, password=self.password)
        new_order = [
                       self.res_one.pk,
                       self.res_three.pk,
                       self.res_two.pk]

        req_data = json.dumps({'new_order': new_order})
        resp = self.client.post(reverse('resources:order', kwargs={
                                        'slug': self.lesson.slug}),
                                        req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(self.lesson.get_resource_order(), map(str, new_order))
        self.assertTrue(resp_data['success'])
