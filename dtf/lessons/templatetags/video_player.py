from django import template
register = template.Library()

@register.inclusion_tag('includes/video_player.html')
def video_player(obj):
    """
    Receives object with 'video' FileField and returns HTML5 player.
    """
    return {'object': obj}