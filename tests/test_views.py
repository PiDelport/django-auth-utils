from unittest import TestCase

from mock_compat import NonCallableMock

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.views.generic import View

from auth_utils.views import ObjectPermissionRequiredMixin


class PermissionView(ObjectPermissionRequiredMixin, View):
    """
    Stub object-permission-protected view.
    """

    permission_required = ['custom.always', 'custom.object']

    _the_object = object()

    def get_object(self, queryset=None):
        assert queryset is None
        return self._the_object

    def get(self, request):
        return 'Permitted!'


class TestObjectPermissionRequiredMixin(TestCase):
    """
    Test `ObjectPermissionRequiredMixin` via PermissionView.

    Set up mocked users, and check their access.
    """

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.view = PermissionView.as_view()

        def has_perms(perms, obj=None):
            return set(perms) <= {
                'custom.always',
                'custom.object' if obj is PermissionView._the_object else 'custom.no_object',
            }
        self.permitted_user = NonCallableMock(spec=[], has_perms=has_perms)
        self.denied_user = NonCallableMock(spec=[], has_perms=lambda perms, obj=None: False)

    def _assertPermitted(self, response):
        assert response == 'Permitted!'

    def _assertNotPermitted(self, response):
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=/'

    def test_anonymous_denied(self):
        self.request.user = AnonymousUser()
        self._assertNotPermitted(self.view(self.request))

    def test_permitted_user(self):
        self.request.user = self.permitted_user
        self._assertPermitted(self.view(self.request))

    def test_denied_user(self):
        self.request.user = self.denied_user
        self._assertNotPermitted(self.view(self.request))
