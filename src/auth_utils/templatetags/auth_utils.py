"""
Auth-related template helpers.
"""
from attr import attributes, attr

from django import template
from django.contrib.auth import get_permission_codename

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


@register.filter
def can_change(user, obj):
    """
    Shortcut for checking if the user has permission to change the given object.
    """
    perm = _get_perm_string('change', obj._meta)
    return user.has_perm(perm, obj)


@register.filter
def can_delete(user, obj):
    """
    Shortcut for checking if the user has permission to delete the given object.
    """
    perm = _get_perm_string('delete', obj._meta)
    return user.has_perm(perm, obj)


def _get_perm_string(action, opts):
    """
    Return the permission string for the given action and model ``_meta`` options.
    """
    codename = get_permission_codename(action, opts)
    return '{}.{}'.format(opts.app_label, codename)
