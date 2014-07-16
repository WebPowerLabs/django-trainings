from django.contrib.sites.models import get_current_site
from django.contrib.contenttypes.models import ContentType

import dtf_comments
from facebook_groups.models import FacebookGroup
DTFComment = dtf_comments.get_model()


def latest_comments(request):
    '''
    returns latest public comments from all models for the active site id
    '''
    purchased_list = []
    for group in FacebookGroup.objects.purchased(request.user):
        purchased_list.append(group.pk)
    site = get_current_site(request)
    content_type_id = ContentType.objects.get_for_model(DTFComment)
    qs = DTFComment.objects.filter(
        site__pk=site.pk,
        is_public=True,
        is_removed=False,
        object_pk__in=purchased_list,
    ).exclude(content_type=content_type_id)  # exclude comment's comments
    return qs.order_by('-submit_date')[:40]
