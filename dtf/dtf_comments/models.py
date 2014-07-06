from django.db.models.fields.related import ForeignKey
from django_comments.models import Comment


class DTFComment(Comment):
    hero_unit = ForeignKey('courses.Content')
