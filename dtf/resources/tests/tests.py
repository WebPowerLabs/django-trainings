from django_nose.testcases import FastFixtureTestCase
from django.contrib.auth.models import User
from resources.models import Resource
from resources.tests.factories import (ResourceFactory, LessonFactory,
                                       UserFactory)
from django.test.client import Client
import json
from django.core.urlresolvers import reverse


class ResourceManagerTest(FastFixtureTestCase):
    def setUp(self):
        self.res_pub = ResourceFactory(published=True)
        self.res_not_pub = ResourceFactory(published=False)
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


class ResourceViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.lesson = LessonFactory()
        self.res_one = ResourceFactory(lesson=self.lesson)
        self.res_two = ResourceFactory(lesson=self.lesson)
        self.res_three = ResourceFactory(lesson=self.lesson)
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_order_view(self):
        self.client.login(username=self.username, password=self.password)
        new_order = [
                       self.res_one.pk,
                       self.res_three.pk,
                       self.res_two.pk]

        req_data = json.dumps({'new_order': new_order})
        resp = self.client.post(reverse('resources:order', kwargs={
                                        'lesson_pk': self.lesson.pk}),
                                        req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(self.lesson.get_resource_order(), map(str, new_order))
        self.assertTrue(resp_data['success'])
