from django_nose.testcases import FastFixtureTestCase
from courses.tests.factories import UserFactory
from django.test.client import Client
from dtf_comments.tests.factories import FacebookGroupFactory, ContentFactory


class DTFCommentViewTest(FastFixtureTestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.client = Client()
        self.user = UserFactory(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        self.content = ContentFactory(owner=self.user)
        self.fb_group = FacebookGroupFactory()

    def test_dtfcomment_share_view(self):
        pass