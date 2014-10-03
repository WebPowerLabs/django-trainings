from django.db.models.fields.related import ForeignKey

from django_comments.models import Comment


class DTFComment(Comment):
    hero_unit = ForeignKey('courses.Content', null=True, blank=True)

    @property
    def content_object_name(self):
        '''
        returns name of content object
        '''
        return self.get_content_object_name()

    def get_content_object_name(self):
        '''
        returns the name of the content object if it exists as 
        content_object.name
        '''
        return self.content_object.name if self.content_object.name else None