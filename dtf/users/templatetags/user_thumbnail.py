from django import template
register = template.Library()

@register.inclusion_tag('includes/_user_thumbnail.html')
def user_thumbnail(user):
    """
    User Thumbnail if facebook if fb_uid else thumnail obj
    """
    return {'user': user}


