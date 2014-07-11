from profiles.models import InstructorProfile
from polymorphic.manager import PolymorphicManager


class ResourceManager(PolymorphicManager):
    def published(self):
        return self.filter(published=True)

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
