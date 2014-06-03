from django_nose.testcases import FastFixtureTestCase
from lessons.tests.factories import TagFactory, LessonFactory, CourseFactory
from lessons.models import Lesson
from django.core.urlresolvers import reverse


class LessonManagerTest(FastFixtureTestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.course = CourseFactory()
        self.first = LessonFactory(tags=[self.tag], course=self.course)
        self.curr = LessonFactory(tags=[self.tag], course=self.course)
        self.last = LessonFactory(tags=[self.tag], course=self.course)

    def test_get_next_url_by_tag(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.last.slug})
        url = Lesson.objects.get_next_url(self.curr, self.tag.id)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_tag(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.first.slug})
        url = Lesson.objects.get_prev_url(self.curr, self.tag.id)
        self.assertEqual(actual_url, url)

    def test_get_next_url_by_course(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.last.slug})
        url = Lesson.objects.get_next_url(obj=self.curr, course_id=self.course.id)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_by_course(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.first.slug})
        url = Lesson.objects.get_prev_url(obj=self.curr, course_id=self.course.id)
        self.assertEqual(actual_url, url)

    def test_get_next_url_all(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.last.slug})
        url = Lesson.objects.get_next_url(obj=self.curr)
        self.assertEqual(actual_url, url)

    def test_get_prev_url_all(self):
        actual_url = reverse('lessons:detail', kwargs={'slug': self.first.slug})
        url = Lesson.objects.get_prev_url(obj=self.curr)
        self.assertEqual(actual_url, url)

    def test_get_next_url_None(self):
        url = Lesson.objects.get_next_url(obj=self.last)
        self.assertFalse(url)

    def test_get_prev_url_None(self):
        url = Lesson.objects.get_prev_url(obj=self.first)
        self.assertFalse(url)
