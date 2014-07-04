from django_comments.models import Comment
from jsonfield import JSONField


class DTFComment(Comment):
    hero_unit = JSONField(null=True, blank=True)
