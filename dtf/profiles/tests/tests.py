from django_nose.testcases import FastFixtureTestCase
from django.test.client import Client
import json
from django.core.urlresolvers import reverse
from profiles.tests.factories import CourseFactory, LessonFactory, UserFactory
from profiles.models import Favourite


class ProfilesViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.course = CourseFactory()
        self.lesson = LessonFactory()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_favourite_add_view_lesson(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('profiles:add_favourite', kwargs={
                                                    'model_name': 'lesson',
                                                    'pk': self.lesson.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertTrue(Favourite.objects.all())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_favourite_add_view_course(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('profiles:add_favourite', kwargs={
                                                    'model_name': 'course',
                                                    'pk': self.course.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertTrue(Favourite.objects.all())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])
