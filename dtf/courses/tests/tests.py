from django_nose.testcases import FastFixtureTestCase
from courses.models import Course, CourseFavourite, CourseHistory
from courses.tests.factories import CourseFactory, UserFactory
from django.contrib.auth.models import User
from django.test.client import Client
import json
from django.core.urlresolvers import reverse


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

    def test_set_order(self):
        new_order = [self.course_not_pub.pk, self.course_pub.pk]
        Course.objects.set_order(new_order)
        self.assertEqual(Course.objects.get_order(), new_order)


class CourseViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.course_one = CourseFactory()
        self.course_two = CourseFactory()
        self.course_three = CourseFactory()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_order_view(self):
        self.client.login(username=self.username, password=self.password)
        new_order = [self.course_one.pk,
                     self.course_three.pk,
                     self.course_two.pk]

        req_data = json.dumps({'new_order': new_order})
        resp = self.client.post(reverse('courses:order'), req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(Course.objects.get_order(), map(str, new_order))
        self.assertTrue(resp_data['success'])

    def test_course_add_favourite_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('courses:add_favourite', kwargs={
                                                    'pk': self.course_one.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertTrue(CourseFavourite.objects.get(
                                    course=self.course_one,
                                    user=self.client.session['_auth_user_id']))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_course_detail_view_create_history_object(self):
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('courses:detail', kwargs={
                                              'slug': self.course_one.slug}))
        self.assertTrue(CourseHistory.objects.get(course=self.course_one,
                                  user=self.client.session['_auth_user_id']))

