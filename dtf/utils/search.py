from elasticsearch import Elasticsearch
from django.conf import settings


class EsClient(object):
    """
    Client for the Elasticsearch.
    """
    def __init__(self, obj=None):
        self.search_index = settings.ELASTICSEARCH_INDEX
        self.client = Elasticsearch(settings.ELASTICSEARCH_SETTINGS)
        self.obj = obj
        self.type = obj.__class__.__name__.lower()

    def get_data(self):
        """
        Returns prepared data for store it in an index.
        """
        return {'name': self.obj.name,
                'description': self.obj.description,
                'url': self.obj.get_absolute_url()}

    def index(self):
        """
        Adds or updates a document in an index.
        """
        return self.client.index(index=self.search_index, doc_type=self.type,
                                 id=self.obj.pk, body=self.get_data())

    def delete(self):
        """
        Delete a document from an index.
        """
        return self.client.delete(index=self.search_index, doc_type=self.type,
                           id=self.obj.pk)

    def search(self, query):
        """
        Executes a search query and get back search hits that match the query.
        """
        res_list = []
        res = self.client.search(index=self.search_index, body={
                                 "query": {"query_string": {"query": query}}})
        for i in res['hits']['hits']:
            item = {'id': i['_id'],
                    'type': i['_type'],
                    'source': i['_source']}
            res_list.append(item)
        return res_list

    def health(self):
        """
        Returns a very simple status on the health of the cluster.
        """
        return self.client.cluster.health()

