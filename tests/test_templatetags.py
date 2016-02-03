from unittest import TestCase
from mock_compat import NonCallableMock

from django.template import Template, Context, TemplateSyntaxError


class TestAuthUtils(TestCase):
    """
    The `auth_utils` template tag library.
    """

    def setUp(self):
        """
        Set up a mock user, with permissions for mock changeable and deletable objects.
        """
        _meta = NonCallableMock(spec=[], app_label='custom', model_name='foo')
        self.changeable = NonCallableMock(spec=[], _meta=_meta)
        self.deletable = NonCallableMock(spec=[], _meta=_meta)

        def has_perm(perm, obj=None):
            return any([
                perm == 'custom.always',
                perm == 'custom.change_foo' and obj is self.changeable,
                perm == 'custom.delete_foo' and obj is self.deletable,
            ])
        self.user = NonCallableMock(spec=[], has_perm=has_perm)

    def _render(self, template_string):
        """
        Render a template string with `auth_utils` loaded.
        """
        return Template('{% load auth_utils %}' + template_string).render(Context({
            'user': self.user,
            'changeable': self.changeable,
            'deletable': self.deletable,
        }))

    def test_smoke(self):
        """
        Loading `auth_utils` doesn't crash.
        """
        self._render('')

    def _assertCondition(self, condition, expected):
        """
        Helper: The template condition string should have the expected logical result.
        """
        template = '{% if ' + condition + ' %}yes{% else %}no{% endif %}'
        assert self._render(template) == ('yes' if expected else 'no')

    def test_perms_reject_unknown(self):
        """
        The `perms` filter is false for unknown permissions.
        """
        for perm in ['""', '"unknown"', 'None']:
            self._assertCondition(perm + ' in user|perms', False)
            self._assertCondition(perm + ' in user|perms:changeable', False)
            self._assertCondition(perm + ' in user|perms:deletable', False)

    def test_perms_always_granted(self):
        """
        The `perms` filter works for always-granted permissions.
        """
        self._assertCondition('"custom.always" in user|perms', True)
        self._assertCondition('"custom.always" in user|perms:changeable', True)
        self._assertCondition('"custom.always" in user|perms:deletable', True)

    def test_perms_per_object(self):
        """
        The `perms` filter works for per-object permissions.
        """
        self._assertCondition('"custom.change_foo" in user|perms', False)
        self._assertCondition('"custom.change_foo" in user|perms:changeable', True)
        self._assertCondition('"custom.change_foo" in user|perms:deletable', False)

        self._assertCondition('"custom.delete_foo" in user|perms', False)
        self._assertCondition('"custom.delete_foo" in user|perms:changeable', False)
        self._assertCondition('"custom.delete_foo" in user|perms:deletable', True)

    def test_can_change(self):
        self._assertCondition('user|can_change:changeable', True)
        self._assertCondition('user|can_change:deletable', False)
        with self.assertRaises(TemplateSyntaxError):
            self._render('{{ user|can_change }}')

    def test_can_delete(self):
        self._assertCondition('user|can_delete:changeable', False)
        self._assertCondition('user|can_delete:deletable', True)

    def test_can_change_can_delete_require_argument(self):
        """
        `can_change` and `can_delete` require an argument.
        """
        for f in ['can_change', 'can_delete']:
            with self.assertRaises(TemplateSyntaxError) as cm:
                self._render('{{ user|' + f + ' }}')
            assert str(cm.exception) == f + ' requires 2 arguments, 1 provided'
