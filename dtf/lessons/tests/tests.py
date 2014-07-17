from django_nose.testcases import FastFixtureTestCase
from lessons.tests.factories import (TagFactory, LessonFactory, CourseFactory,
                                     UserFactory, LessonHistoryFactory,
                                     LessonFavouriteFactory,
                                     InstructorProfileFactory, PackageFactory,
                                     PackagePurchaseFactory)
from lessons.models import Lesson, LessonFavourite, LessonHistory
from django.core.urlresolvers import reverse
from django.test.client import Client
import json
from utils.tests import TestCaseBase


class LessonViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.course = CourseFactory(owner=self.user)
        self.lesson_one = LessonFactory(course=self.course,
                                        owner=self.user)
        self.lesson_two = LessonFactory(course=self.course, owner=self.user)
        self.lesson_three = LessonFactory(course=self.course, owner=self.user)
        self.lesson_his_item = LessonHistoryFactory(user=self.user,
                                                    lesson=self.lesson_two,
                                                    is_active=True)
        self.lesson_fav_item = LessonFavouriteFactory(user=self.user,
                                                      lesson=self.lesson_one,
                                                      is_active=True)

    def test_order_view(self):
        self.client.login(username=self.username, password=self.password)
        new_order = [self.lesson_three.pk,
                     self.lesson_one.pk,
                     self.lesson_two.pk]

        req_data = json.dumps({'new_order': new_order})
        resp = self.client.post(reverse('lessons:order', kwargs={
                                        'slug': self.course.slug}),
                                        req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertEqual(self.course.get_lesson_order(), map(str, new_order))
        self.assertTrue(resp_data['success'])

    def test_lesson_action_favourite_view_add_item(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('lessons:favourite_action', kwargs={
                                                    'pk': self.lesson_one.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertTrue(LessonFavourite.objects.get(
                                    lesson=self.lesson_one,
                                    user=self.client.session['_auth_user_id']))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_lesson_favourite_action_view_delete_item(self):
        self.client.login(username=self.username, password=self.password)

        resp = self.client.post(reverse('lessons:favourite_action', kwargs={
                                                    'pk': self.lesson_one.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        deleted_item = LessonFavourite.objects.get(pk=self.lesson_fav_item.pk)
        self.assertFalse(deleted_item.is_active)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_lesson_detail_view_create_history_object(self):
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('lessons:detail', kwargs={
                                              'slug': self.lesson_one.slug}))
        self.assertTrue(LessonHistory.objects.get(lesson=self.lesson_one,
                                  user=self.client.session['_auth_user_id']))

    def test_lesson_history_delete_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('lessons:delete_history', kwargs={
                                            'pk': self.lesson_his_item.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        deleted_item = LessonHistory.objects.get(pk=self.lesson_his_item.pk)
        self.assertFalse(deleted_item.is_active)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])


class LessonManagerTest(TestCaseBase):
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
        self.tag = TagFactory()
        self.course_pub = CourseFactory(published=True, owner=self.instructor)
        self.course_not_pub = CourseFactory(published=False,
                                            owner=self.instructor)
        self.lesson_of_not_pub_course = LessonFactory(published=True,
                                                  course=self.course_not_pub,
                                                  owner=self.instructor)
        self.lesson_first_pub = LessonFactory(tags=[self.tag],
                                              course=self.course_pub,
                                              published=True,
                                              owner=self.instructor)
        self.lesson_curr_not_pub = LessonFactory(tags=[self.tag],
                                                 course=self.course_pub,
                                                 published=False,
                                                 owner=self.instructor)
        self.lesson_last_pub = LessonFactory(tags=[self.tag],
                                             course=self.course_pub,
                                             published=True,
                                             owner=self.instructor)
        self.package = PackageFactory()
        self.package.lessons.add(self.lesson_curr_not_pub)

        self.package_user = PackageFactory()
        self.package_user.lessons.add(self.lesson_first_pub)
        self.package_user.courses.add(self.course_not_pub)
        self.package_purchased = PackagePurchaseFactory(user=self.user,
                                                    package=self.package_user,
                                                    status=1)

    def test_purchased(self):
        purchased = [self.lesson_of_not_pub_course,
                     self.lesson_first_pub,
                     self.lesson_last_pub]
        res = Lesson.objects.purchased(self.user)
        self.assertEqualQs(res, purchased)

    def test_get_list_user_had_insrtuctor_profile(self):
        total_count = Lesson.objects.all().count()
        current_count = Lesson.objects.get_list(self.instructor).count()
        self.assertEqual(total_count, current_count)

    # User is staff
    def test_get_list_user_is_staff(self):
        total_count = Lesson.objects.all().count()
        current_count = Lesson.objects.get_list(self.staff_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_next_url_by_tag_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          tag_id=self.tag.id,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          tag_id=self.tag.id,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          course_id=self.course_pub.id,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          course_id=self.course_pub.id,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all_user_is_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_curr_not_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          user=self.staff_user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None_user_is_staff(self):
        url = Lesson.objects.get_next_url(obj=self.lesson_of_not_pub_course,
                                          user=self.staff_user)
        self.assertFalse(url)

    def test_get_prev_url_None_user_is_staff(self):
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          user=self.staff_user)
        self.assertFalse(url)

    # User is not staff
    def test_get_list_user_is_not_staff(self):
        total_count = Lesson.objects.published().filter(
                                             course__published=True).count()
        current_count = Lesson.objects.get_list(self.user).count()
        self.assertEqual(total_count, current_count)

    def test_get_next_url_by_tag_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          tag_id=self.tag.id,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                         'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          tag_id=self.tag.id,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                         'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          course_id=self.course_pub.id,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          course_id=self.course_pub.id,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                        'slug': self.lesson_first_pub.slug})
        url = Lesson.objects.get_next_url(obj=self.lesson_last_pub,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all_user_is_not_staff(self):
        actual_url = reverse('lessons:detail', kwargs={
                                         'slug': self.lesson_last_pub.slug})
        url = Lesson.objects.get_prev_url(obj=self.lesson_first_pub,
                                          user=self.user)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None_user_is_not_staff(self):
        url = Lesson.objects.get_next_url(obj=self.lesson_first_pub,
                                          user=self.user)
        self.assertFalse(url)

    def test_get_prev_url_None_user_is_not_staff(self):
        url = Lesson.objects.get_prev_url(obj=self.lesson_last_pub,
                                          user=self.user)
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
