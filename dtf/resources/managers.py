from profiles.models import InstructorProfile
from polymorphic.manager import PolymorphicManager
from django.db.models import Q, Count


class ResourceManager(PolymorphicManager):
    def published(self):
        return self.filter(published=True)

    def purchased(self, user):
        return self.annotate(Count('lesson__package'),
                             Count('lesson__course__package')
                     ).filter(Q(lesson__package__packagepurchase__user=user,
                        lesson__package__packagepurchase__status=1) |
                      Q(lesson__course__package__packagepurchase__user=user,
                        lesson__course__package__packagepurchase__status=1) |
                      Q(lesson__package__count=0,
                        lesson__course__package__count=0)).distinct()

    def get_list(self, user=None):
        """
        Returns object list all() if user is staff or published() if not.
        """
        if user and user.is_authenticated():
            try:
                instructor = user.instructorprofile
            except InstructorProfile.DoesNotExist:
                instructor = False
            if user.is_staff or instructor:
                return self.all()
        return self.published().filter(lesson__published=True)
