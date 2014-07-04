from django.contrib.sites.models import get_current_site
from django.contrib.contenttypes.models import ContentType

import dtf_comments
DTFComment = dtf_comments.get_model()


def latest_comments(request):
    '''
    returns latest public comments from all models for the active site id
    '''
    site = get_current_site(request)
    content_type_id = ContentType.objects.get_for_model(DTFComment)
    qs = DTFComment.objects.filter(
        site__pk=site.pk,
        is_public=True,
        is_removed=False,
    ).exclude(content_type=content_type_id)  # exclude comment's comments
    return qs.order_by('-submit_date')[:40]
