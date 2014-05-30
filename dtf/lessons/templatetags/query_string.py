from django import template
from copy import deepcopy
from django.http.request import QueryDict
register = template.Library()


@register.simple_tag
def query_string(source=None, **kwargs):
    q = QueryDict('', True)
    if source:
        q.update(source)
    for k, v in kwargs.items():
        q.update({k: v})
    if q:
        return "{}".format('?' + q.urlencode())
    return q.urlencode()
