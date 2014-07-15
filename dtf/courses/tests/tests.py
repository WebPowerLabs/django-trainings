from django.db.models import Q
from django_nose.testcases import FastFixtureTestCase
from courses.models import Course, CourseFavourite, CourseHistory
from courses.tests.factories import (CourseFactory, UserFactory,
                                     CourseFavouriteFactory,
                                     CourseHistoryFactory,
                                     InstructorProfileFactory, PackageFactory,
                                     LessonFactory, PackagePurchaseFactory)
from django.test.client import Client
import json
from django.core.urlresolvers import reverse
from utils.tests import TestCaseBase


class CourseManagerTest(TestCaseBase):
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
        self.course_pub = CourseFactory(published=True, owner=self.instructor)
        self.course_not_pub = CourseFactory(published=False,
                                            owner=self.instructor)
        self.course_purchased = CourseFactory(published=True,
                                              owner=self.instructor)
        self.lesson = LessonFactory(course=self.course_purchased,
                                    owner=self.instructor)
        self.lesson_two = LessonFactory(course=self.course_pub,
                                        owner=self.instructor)
        self.package = PackageFactory()
        self.package.lessons.add(self.lesson_two)

        self.package.courses.add(self.course_purchased)
        self.package_purchased = PackagePurchaseFactory(user=self.user,
                                                        package=self.package,
                                                        status=1)

    def test_purchased(self):
        purchased = [self.course_purchased]
        res = Course.objects.purchased(self.user)
        self.assertEqualQs(res, purchased)

    def test_get_list_user_had_insrtuctor_profile(self):
        total_count = Course.objects.all().count()
        current_count = Course.objects.get_list(self.instructor).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_user_is_staff(self):
        total_count = Course.objects.all().count()
        current_count = Course.objects.get_list(self.staff_user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_user_is_not_staff(self):
        total_count = Course.objects.published().count()
        current_count = Course.objects.get_list(self.user).count()
        self.assertEqual(total_count, current_count)

    def test_get_list_no_user(self):
        total_count = Course.objects.published().count()
        current_count = Course.objects.get_list().count()
        self.assertEqual(total_count, current_count)

    def test_set_order(self):
        new_order = [self.course_not_pub.pk, self.course_pub.pk,
                     self.course_purchased.pk]
        Course.objects.set_order(new_order)
        self.assertEqual(Course.objects.get_order(), new_order)


class CourseViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.course_one = CourseFactory(owner=self.user)
        self.course_two = CourseFactory(owner=self.user)
        self.course_three = CourseFactory(owner=self.user)
        self.course_his_item = CourseHistoryFactory(user=self.user,
                                                    course=self.course_two,
                                                    is_active=True)
        self.course_fav_item = CourseFavouriteFactory(user=self.user,
                                                      course=self.course_one,
                                                      is_active=True)

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

    def test_course_favourite_action_view_add_item(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('courses:favourite_action', kwargs={
                                                    'pk': self.course_one.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        self.assertTrue(CourseFavourite.objects.get(
                                    course=self.course_one,
                                    user=self.client.session['_auth_user_id']))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_course_favourite_action_view_delete_item(self):
        self.client.login(username=self.username, password=self.password)

        resp = self.client.post(reverse('courses:favourite_action', kwargs={
                                                    'pk': self.course_one.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        deleted_item = CourseFavourite.objects.get(pk=self.course_fav_item.pk)
        self.assertFalse(deleted_item.is_active)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])

    def test_course_detail_view_create_history_object(self):
        self.client.login(username=self.username, password=self.password)
        self.client.get(reverse('courses:detail', kwargs={
                                              'slug': self.course_one.slug}))
        self.assertTrue(CourseHistory.objects.get(course=self.course_one,
                                  user=self.client.session['_auth_user_id']))

    def test_course_history_delete_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('courses:delete_history', kwargs={
                                            'pk': self.course_his_item.pk}),
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                        content_type='application/json')
        resp_data = json.loads(resp.content)
        deleted_item = CourseHistory.objects.get(pk=self.course_his_item.pk)
        self.assertFalse(deleted_item.is_active)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp_data['success'])
