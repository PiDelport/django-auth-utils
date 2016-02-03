"""
Django authentication backend implementation helpers.
"""


class BaseAuthorizationBackend:
    """
    Base implementation of an authorization backend.
    """

    def authenticate(self):
        """
        Does nothing.
        """
        return None

    def get_user(self, user_id):
        """
        Does nothing.
        """
        return None

    def get_user_permissions(self, user_obj, obj=None):
        """
        Extend this to grant additional user-based permissions.
        """
        return set()

    def get_group_permissions(self, user_obj, obj=None):
        """
        Extend this to grant additional group-based permissions.
        """
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        """
        Base implementation of `get_all_permissions()`,
        based on `get_user_permissions()` and `get_group_permissions()`.
        """
        if not user_obj.is_active:
            return set()
        else:
            user_perms = self.get_user_permissions(user_obj, obj)
            group_perms = self.get_group_permissions(user_obj, obj)
            return user_perms | group_perms

    def has_perm(self, user_obj, perm, obj=None):
        """
        Base implementation of `has_perm()`, based on `get_all_permissions()`.
        """
        # Referenced from ModelBackend.has_perm()
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Base implementation of `has_module_perms()`, using `get_all_permissions()`.
        """
        # Referenced from ModelBackend.has_module_perms()
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False
