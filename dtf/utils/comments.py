import django_comments

from django.contrib.sites.models import get_current_site


def latest_comments(request):
    '''
    returns latest public comments from all models for the active site id
    '''
    site = get_current_site(request)
    qs = django_comments.get_model().objects.filter(
        site__pk = site.pk,
        is_public = True,
        is_removed = False,
    )
    return qs.order_by('-submit_date')[:40] 
