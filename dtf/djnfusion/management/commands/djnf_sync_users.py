from django.core.management.base import BaseCommand
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from djnfusion import sync_user



class Command(BaseCommand):

    help = 'Synchronizes all users with infusionsoft.'

    def handle(self, *args, **options):

        for u in User.objects.all():
            print "Synchronizing user %s / %s ..." % (u.id, u.email)
            if sync_user(user=u):
                print "Successful."



