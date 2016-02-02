from unittest import TestCase
from mock_compat import NonCallableMock

from auth_utils.backends import BaseAuthorizationBackend


class TestDefaultBaseAuthorizationBackend(TestCase):
    """
    The behavior of a default, unspecialized `BaseAuthorizationBackend`.
    """

    def setUp(self):
        self.backend = BaseAuthorizationBackend()
        self.active_user = NonCallableMock(spec=[], is_active=True)
        self.inactive_user = NonCallableMock(spec=[], is_active=False)
        self.users = [self.active_user, self.inactive_user]

    def test_get_permissions(self):
        """
        The ``get_*_permissions()`` methods return no permissions.
        """
        permission_methods = [
            self.backend.get_user_permissions,
            self.backend.get_group_permissions,
            self.backend.get_all_permissions,
        ]
        users = [self.active_user, self.inactive_user]
        for method in permission_methods:
            for user in users:
                assert method(user) == set()
                assert method(user, None) == set()
                assert method(user, object()) == set()

    def test_has_perm(self):
        """
        `has_perm()` always returns false.
        """
        for user in self.users:
            for perm in [None, '', 'dummy']:
                assert self.backend.has_perm(user, perm) is False
                assert self.backend.has_perm(user, perm, None) is False
                assert self.backend.has_perm(user, perm, object()) is False

    def test_has_module_perms(self):
        """
        `has_module_perm()` always returns false.
        """
        for user in self.users:
            for app_label in [None, '', 'dummy', 'app.perm']:
                assert self.backend.has_module_perms(user, app_label) is False


class CustomAuthorizationBackend(BaseAuthorizationBackend):
    """
    See `TestCustomAuthorizationBackend`.
    """

    def get_user_permissions(self, user_obj, obj=None):
        return {self._synthesize_perm('user', user_obj, obj)}

    def get_group_permissions(self, user_obj, obj=None):
        return {self._synthesize_perm('group', user_obj, obj)}

    def _synthesize_perm(self, kind, user_obj, obj):
        return 'custom.{}_{}_{}'.format(
            kind,
            'active' if user_obj.is_active else 'inactive',
            'none' if obj is None else 'obj',
        )


class TestCustomAuthorizationBackend(TestCase):
    """
    The behavior of a `BaseAuthorizationBackend` subclass.
    """

    def setUp(self):
        self.backend = CustomAuthorizationBackend()
        self.active_user = NonCallableMock(spec=[], is_active=True)
        self.inactive_user = NonCallableMock(spec=[], is_active=False)

    def test_get_all_permissions(self):
        """
        `get_all_permissions()` merges the available permissions for active users.
        """
        assert self.backend.get_all_permissions(self.inactive_user) == set()
        assert self.backend.get_all_permissions(self.inactive_user, object()) == set()
        assert self.backend.get_all_permissions(self.active_user) == {
            'custom.user_active_none',
            'custom.group_active_none',
        }
        assert self.backend.get_all_permissions(self.active_user, object()) == {
            'custom.user_active_obj',
            'custom.group_active_obj',
        }

    def test_has_perm(self):
        """
        `has_perm()` agrees with `get_all_permissions()`.
        """
        no_obj_perms = {
            'custom.user_active_none',
            'custom.group_active_none',
        }
        obj_perms = {
            'custom.user_active_obj',
            'custom.group_active_obj',
        }
        for perm in no_obj_perms | obj_perms:
            assert self.backend.has_perm(self.inactive_user, perm) is False
            assert self.backend.has_perm(self.inactive_user, perm, object()) is False

        for perm in no_obj_perms:
            assert self.backend.has_perm(self.active_user, perm) is True
            assert self.backend.has_perm(self.active_user, perm, object()) is False

        for perm in obj_perms:
            assert self.backend.has_perm(self.active_user, perm) is False
            assert self.backend.has_perm(self.active_user, perm, object()) is True

    def test_has_module_perms(self):
        """
        `has_module_perms()` returns true for 'custom', for active users.
        """
        assert self.backend.has_module_perms(self.inactive_user, 'decoy') is False
        assert self.backend.has_module_perms(self.active_user, 'decoy') is False
        assert self.backend.has_module_perms(self.inactive_user, 'custom') is False
        assert self.backend.has_module_perms(self.active_user, 'custom') is True
