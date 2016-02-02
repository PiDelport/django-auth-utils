"""
Auth-related view utils.
"""
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class ObjectPermissionRequiredMixin(PermissionRequiredMixin, SingleObjectMixin):
    """
    Like `PermissionRequiredMixin`, but check the permission against `SingleObjectMixin`'s object.
    """

    def has_permission(self):
        perms = self.get_permission_required()
        obj = self.get_object()
        return self.request.user.has_perms(perms, obj)
