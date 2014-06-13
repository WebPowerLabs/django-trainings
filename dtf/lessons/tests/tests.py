from django_nose.testcases import FastFixtureTestCase
from lessons.tests.factories import (TagFactory, LessonFactory, CourseFactory,
                                     UserFactory)
from lessons.models import Lesson
from django.core.urlresolvers import reverse
from django.test.client import Client
from users.models import User
import json


class LessonViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.course = CourseFactory()
        self.lesson_one = LessonFactory(course=self.course)
        self.lesson_two = LessonFactory(course=self.course)
        self.lesson_three = LessonFactory(course=self.course)
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_order_view(self):
        self.client.login(username=self.username, password=self.password)
        new_order = [self.lesson_one.pk,
                     self.lesson_three.pk,
                     self.lesson_two.pk]

        req_data = json.dumps({'new_order': new_order})
        resp = self.client.post(reverse('lessons:order', kwargs={
                                        'course_pk': self.course.pk}),
                                        req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(self.course.get_lesson_order(), map(str, new_order))
        self.assertTrue(resp_data['success'])


class LessonManagerTest(FastFixtureTestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.course_pub = CourseFactory(published=True)
        self.course_not_pub = CourseFactory(published=False)
        self.lesson_of_not_pub_course = LessonFactory(published=True,
                                                  course=self.course_not_pub)
        self.lesson_first_pub = LessonFactory(tags=[self.tag],
                                              course=self.course_pub,
                                              published=True)
        self.lesson_curr_not_pub = LessonFactory(tags=[self.tag],
                                                 course=self.course_pub,
                                                 published=False)
        self.lesson_last_pub = LessonFactory(tags=[self.tag],
                                             course=self.course_pub,
                                             published=True)
        self.fake_staff_user = User(username="staff", is_staff=True)
        self.fake_user = User(username="user", is_staff=False)

    # User is staff
    def test_get_list_user_is_staff(self):
        total_count = Lesson.objects.all().count()
        current_count = Lesson.objects.get_list(self.fake_staff_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_next_url_by_tag_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          tag_id=self.tag.id,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          tag_id=self.tag.id,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          course_id=self.course_pub.id,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          course_id=self.course_pub.id,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          user=self.fake_staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None_user_is_staff(self):
        url = Lesson.objects.get_next_url(obj=self.lesson_of_not_pub_course,
                                          user=self.fake_staff_user)
        self.assertFalse(url)

    def test_get_prev_url_None_user_is_staff(self):
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          user=self.fake_staff_user)
        self.assertFalse(url)

    # User is not staff
    def test_get_list_user_is_not_staff(self):
        total_count = Lesson.objects.published().filter(
                                                 course__published=True).count()
        current_count = Lesson.objects.get_list(self.fake_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_next_url_by_tag_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          tag_id=self.tag.id,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          tag_id=self.tag.id,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          course_id=self.course_pub.id,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          course_id=self.course_pub.id,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          user=self.fake_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None_user_is_not_staff(self):
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          user=self.fake_user)
        self.assertFalse(url)

    def test_get_prev_url_None_user_is_not_staff(self):
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          user=self.fake_user)
        self.assertFalse(url)

    # No user
    def test_get_list_no_user(self):
        total_count = Lesson.objects.published().filter(
                                                 course__published=True).count()
        current_count = Lesson.objects.get_list().count()
        self.assertEqual(total_count, current_count)

    def test_get_next_url_by_tag_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          tag_id=self.tag.id)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          tag_id=self.tag.id)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          course_id=self.course_pub.id)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          course_id=self.course_pub.id)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                            'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all_no_user(self):
        actual_url = reverse('lessons:detail', kwargs={
                                             'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None_no_user(self):
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub)
        self.assertFalse(url)

    def test_get_prev_url_None_no_user(self):
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub)
        self.assertFalse(url)
