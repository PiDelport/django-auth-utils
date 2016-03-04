"""
Backported tests for the Django 1.8 compatibility code.
"""
from django.contrib.auth import models
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.http import HttpResponse
from django.views.generic import View

from auth_utils.django18_compat import PermissionRequiredMixin

from django.test import RequestFactory, TestCase, override_settings


# Used by PermissionsRequiredMixinTests
class EmptyResponseView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse()


class PermissionsRequiredMixinTests(TestCase):
    """
    Backported from Django 1.9's tests/auth_tests/test_mixins.py

    Backport changes:

        * Permission names: {add,change}_customuser -> {add,change}_user
    """

    factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = models.User.objects.create(username='joe', password='qwerty')
        perms = models.Permission.objects.filter(codename__in=('add_user', 'change_user'))
        assert perms
        cls.user.user_permissions.add(*perms)

    def test_many_permissions_pass(self):
        class AView(PermissionRequiredMixin, EmptyResponseView):
            permission_required = ['auth.add_user', 'auth.change_user']

        request = self.factory.get('/rand')
        request.user = self.user
        resp = AView.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    def test_single_permission_pass(self):
        class AView(PermissionRequiredMixin, EmptyResponseView):
            permission_required = 'auth.add_user'

        request = self.factory.get('/rand')
        request.user = self.user
        resp = AView.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    def test_permissioned_denied_redirect(self):
        class AView(PermissionRequiredMixin, EmptyResponseView):
            permission_required = ['auth.add_user', 'auth.change_user', 'non-existent-permission']

        request = self.factory.get('/rand')
        request.user = self.user
        resp = AView.as_view()(request)
        self.assertEqual(resp.status_code, 302)

    def test_permissioned_denied_exception_raised(self):
        class AView(PermissionRequiredMixin, EmptyResponseView):
            permission_required = ['auth.add_user', 'auth.change_user', 'non-existent-permission']
            raise_exception = True

        request = self.factory.get('/rand')
        request.user = self.user
        self.assertRaises(PermissionDenied, AView.as_view(), request)


class ExtraTests(TestCase):
    """
    These are a few extra tests to cover what the backported tests miss.
    """

    def setUp(self):
        class AView(PermissionRequiredMixin, EmptyResponseView):
            pass
        self.view = AView()

    @override_settings(LOGIN_URL=None)
    def test_get_login_url_ImproperlyConfigured(self):
        with self.assertRaises(ImproperlyConfigured) as cm:
            self.view.get_login_url()

        self.assertEqual(str(cm.exception), (
            'AView is missing the login_url attribute.'
            ' Define AView.login_url, settings.LOGIN_URL, or override AView.get_login_url().'
        ))

    def test_get_permission_required_ImproperlyConfigured(self):
        with self.assertRaises(ImproperlyConfigured) as cm:
            self.view.get_permission_required()

        self.assertEqual(str(cm.exception), (
            'AView is missing the permission_required attribute.'
            ' Define AView.permission_required, or override AView.get_permission_required().'
        ))
