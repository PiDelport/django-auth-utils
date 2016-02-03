"""
Django 1.8 backward compatibility.
"""
# flake8: noqa
import django

__all__ = ['PermissionRequiredMixin']


if (1, 9) <= django.VERSION:
    from django.contrib.auth.mixins import PermissionRequiredMixin
else:
    # The following code referenced wholesale from Django 1.9.0.

    from django.conf import settings
    from django.contrib.auth import REDIRECT_FIELD_NAME
    from django.contrib.auth.views import redirect_to_login
    from django.core.exceptions import ImproperlyConfigured, PermissionDenied
    from django.utils import six
    from django.utils.encoding import force_text


    class AccessMixin(object):
        """
        Abstract CBV mixin that gives access mixins the same customizable
        functionality.
        """
        login_url = None
        permission_denied_message = ''
        raise_exception = False
        redirect_field_name = REDIRECT_FIELD_NAME

        def get_login_url(self):
            """
            Override this method to override the login_url attribute.
            """
            login_url = self.login_url or settings.LOGIN_URL
            if not login_url:
                raise ImproperlyConfigured(
                    '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                    '{0}.get_login_url().'.format(self.__class__.__name__)
                )
            return force_text(login_url)

        def get_permission_denied_message(self):
            """
            Override this method to override the permission_denied_message attribute.
            """
            return self.permission_denied_message

        def get_redirect_field_name(self):
            """
            Override this method to override the redirect_field_name attribute.
            """
            return self.redirect_field_name

        def handle_no_permission(self):
            if self.raise_exception:
                raise PermissionDenied(self.get_permission_denied_message())
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


    class PermissionRequiredMixin(AccessMixin):
        """
        CBV mixin which verifies that the current user has all specified
        permissions.
        """
        permission_required = None

        def get_permission_required(self):
            """
            Override this method to override the permission_required attribute.
            Must return an iterable.
            """
            if self.permission_required is None:
                raise ImproperlyConfigured(
                    '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                    '{0}.get_permission_required().'.format(self.__class__.__name__)
                )
            if isinstance(self.permission_required, six.string_types):
                perms = (self.permission_required,)
            else:
                perms = self.permission_required
            return perms

        def has_permission(self):
            """
            Override this method to customize the way permissions are checked.
            """
            perms = self.get_permission_required()
            return self.request.user.has_perms(perms)

        def dispatch(self, request, *args, **kwargs):
            if not self.has_permission():
                return self.handle_no_permission()
            return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
