"""
Auth-related template helpers.
"""
from attr import attributes, attr

from django import template

register = template.Library()


@register.filter
def perms(user, obj=None):
    """
    Allow checking the user's permissions, optionally on the given object.

    This returns a permission-checking helper which provides templates the equivalent of
    ``user.has_perm(perm, obj)``, using the following syntax::

        {% if perm in user|perms:obj %}
    """
    return PermChecker(user, obj)


@attributes
class PermChecker(object):
    """
    Permission-checking helper.

    This is similar to `django.contrib.auth.context_processors.PermWrapper`,
    but supports object permissions.
    """
    user = attr()
    obj = attr()

    def __contains__(self, perm):
        return self.user.has_perm(perm, self.obj)
