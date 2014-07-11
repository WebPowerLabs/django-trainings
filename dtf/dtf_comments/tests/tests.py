from django_nose.testcases import FastFixtureTestCase
from courses.tests.factories import UserFactory
from django.test.client import Client
from dtf_comments.tests.factories import FacebookGroupFactory, ContentFactory
from django.core.urlresolvers import reverse
from dtf_comments.models import DTFComment
from django.contrib.contenttypes.models import ContentType


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

    def test_dtf_comment_share_view(self):
        content_type = ContentType.objects.get_for_model(self.fb_group)
        req_data = {'comment': 'test text', 'object_pk': self.fb_group.pk}
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse('dtf_comments:share',
                                        kwargs={'content_pk': self.content.pk}
                                        ), req_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(DTFComment.objects.get(content_type=content_type,
                                               object_pk=self.fb_group.pk,
                                               hero_unit=self.content))
