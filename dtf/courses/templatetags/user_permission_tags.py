from django import template
register = template.Library()


@register.filter
def can_manage_content(user, content):
    """
    Returns True if user is staff or instructor(owner).
    """
    if user.is_authenticated():
        owner = user == content.course.owner
        if user.is_staff or owner:
            return True
    return False


@register.filter
def is_member(user):
    """
    Returns True if user is not stuff, instructor.
    """
    if user.is_authenticated() and not user.is_staff and not user.is_instructor:
        return True
    return False
