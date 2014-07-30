from courses.models import Content
from facebook_groups.models import FacebookGroup
from django.core.management.base import BaseCommand
from optparse import make_option
from utils.search import EsClient


class Command(BaseCommand):
    help = 'Commands for the Elasticsearch client.'
    option_list = BaseCommand.option_list + (
                make_option('--sync', '-s',
                            action='store_true',
                            dest='sync',
                            default=False,
                            help='Sync db data with cluster.'),
                make_option('--info', '-i',
                             action='store_true',
                             dest='info',
                             default=False,
                             help='Index info.'))

    def handle(self, *args, **options):
        if options.get('sync', None):
            self.sync()

        if options.get('info', None):
            self.info()

    def info(self):
        """
        Displays the doduments info of the index.
        """
        for k, v in EsClient().index_info()['docs'].items():
            self.stdout.write('{}: {}'.format(k.replace('_', ' '), v))

    def sync(self):
        """
        Adds or updates a documents in an index with the db data.
        """
        content_list = Content.objects.all()
        group_list = FacebookGroup.objects.all()
        total_cnt = content_list.count() + group_list.count()
        current_obj_index = 1
        created_cnt = 0
        progress_message = 'Syncing {} of {} item(s)'

        for content in content_list:
            if not content.polymorphic_ctype.name == 'resource':
                self.stdout.write(progress_message.format(current_obj_index,
                                                          total_cnt))
                res = EsClient(content).index()
                created_cnt += 1 if res['created'] else 0
                current_obj_index += 1

        for group in group_list:
            self.stdout.write(progress_message.format(current_obj_index,
                                                      total_cnt))
            res = EsClient(group).index()
            created_cnt += 1 if res['created'] else 0
            current_obj_index += 1
        self.stdout.write('Created: {0}. Updated: {2}. Total: {1}'.format(
                                                      created_cnt, total_cnt,
                                                      total_cnt - created_cnt))
