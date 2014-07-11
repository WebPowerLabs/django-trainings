from django.core.management.base import BaseCommand, CommandError

from djnfusion import server, key

class Command(BaseCommand):

    help = 'Tries to find a user by email.'

    def handle(self, *args, **options):

        try:
            email = args[0]
        except IndexError:
            raise CommandError("Pass email address as parameter.")

        results = server.DataService.findByField(key, "Contact", 10, 0, "email", email, ["Id", "Email"]);
        #results = server.DataService.findByField(key, "SubscriptionPlan", 10, 0, "productid", 37, ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount", "Prorate", "Active", "PlanPrice"]);
        
        print "Found %d results." % len(results)
        for r in results:
            print r

