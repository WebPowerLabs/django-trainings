from courses.models import Content
from facebook_groups.models import FacebookGroup
from django.core.management.base import BaseCommand
from optparse import make_option
from utils.search import EsClient


class Command(BaseCommand):
    help = 'Commands for the Elasticsearch client.'
    option_list = BaseCommand.option_list + (
                make_option('--sync',
                            action='store_true',
                            dest='sync',
                            default=False,
                            help='Sync db data with cluster.'),
                make_option('--health',
                             action='store_true',
                             dest='health',
                             default=False,
                             help='Cluster health info.'))

    def handle(self, *args, **options):
        if options.get('sync', None):
            self.sync()

        if options.get('health', None):
            self.health()

    def health(self):
        """
        Displays a very simple status on the health of the cluster.
        """
        max_len = 80
        for k, v in EsClient().health().items():
            self.stdout.write('{}:{}'.format(k, str(v).rjust(max_len - len(k),
                                                             "_")))

    def sync(self):
        """
        Adds or updates a documents in an index with the db data.
        """
        created_cnt = 0
        total_cnt = 0
        for content in Content.objects.all():
            if not content.polymorphic_ctype.name == 'resource':
                res = EsClient(content).index()
                created_cnt += 1 if res['created'] else 0
                total_cnt += 1
        for group in FacebookGroup.objects.all():
            res = EsClient(group).index()
            created_cnt += 1 if res['created'] else 0
            total_cnt += 1
        self.stdout.write('Created: {0}. Updated: {2}. Total: {1}'.format(
                                                      created_cnt, total_cnt,
                                                      total_cnt - created_cnt))
