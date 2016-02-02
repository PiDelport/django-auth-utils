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
                assert self.backend.has_perm(user, perm) == False
                assert self.backend.has_perm(user, perm, None) == False
                assert self.backend.has_perm(user, perm, object()) == False

    def test_has_module_perms(self):
        """
        `has_module_perm()` always returns false.
        """
        for user in self.users:
            for app_label in [None, '', 'dummy', 'app.perm']:
                assert self.backend.has_module_perms(user, app_label) == False
