from django.db import models
from django.db.models import Q, Count



class JournalQuestionManager(models.Manager):

    def published(self):
        return self.filter(published=True)

    def purchased(self, user):
        return self.annotate(Count('package')
                             ).filter(Q(package__packagepurchase__user=user,
                                        package__packagepurchase__status=1) |
                                      Q(package__count=0), active=True)