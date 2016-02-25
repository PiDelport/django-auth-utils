=================
django-auth-utils
=================

Django authentication and authorization utilities.

.. image:: https://img.shields.io/pypi/v/django-auth-utils.svg
    :target: https://pypi.python.org/pypi/django-auth-utils

.. image:: https://img.shields.io/badge/source-GitHub-lightgrey.svg
    :target: https://github.com/pjdelport/django-auth-utils

.. image:: https://img.shields.io/github/issues/pjdelport/django-auth-utils.svg
    :target: https://github.com/pjdelport/django-auth-utils/issues?q=is:open

.. image:: https://travis-ci.org/pjdelport/django-auth-utils.svg?branch=master
    :target: https://travis-ci.org/pjdelport/django-auth-utils

.. image:: https://codecov.io/github/pjdelport/django-auth-utils/coverage.svg?branch=master
    :target: https://codecov.io/github/pjdelport/django-auth-utils?branch=master

.. contents::

Installation
============

.. code:: shell

    pip install django-auth-utils

Supported and tested on:

* Python: 2.7, 3.4, 3.5, PyPy
* Django: 1.8, 1.9


Configuration
=============

In order to use the ``auth_utils`` template tag library, add ``auth_utils`` to your ``INSTALLED_APPS``.

Alternatively, since Django 1.9, you can add ``auth_utils.templatetags.auth_utils`` to your
DjangoTemplates_ OPTIONS.


.. _DjangoTemplates:
    https://docs.djangoproject.com/en/1.9/topics/templates/#django.template.backends.django.DjangoTemplates


Usage
=====


Permission-checking views
-------------------------

The ``ObjectPermissionRequiredMixin`` view combines Django's PermissionRequiredMixin_ and
SingleObjectMixin_ views, and performs the permission check against the object that was looked up.

.. _PermissionRequiredMixin:
    https://docs.djangoproject.com/en/1.9/topics/auth/default/#the-permissionrequiredmixin-mixin

.. _SingleObjectMixin:
    https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-single-object/#singleobjectmixin

Use it like the base classes:

.. code:: python

    from auth_utils.views import ObjectPermissionRequiredMixin


    class ArticleDetail(ObjectPermissionRequiredMixin, generic.DetailView):
        model = Article
        permission_required = ['news.read_article']


    class ArticleUpdate(ObjectPermissionRequiredMixin, generic.UpdateView):
        model = Article
        permission_required = ['news.change_article']


Permission-checking in templates
--------------------------------

Load the template tag library:

.. code:: django

    {% load auth_utils %}

The ``perms`` filter allows checking object-level permissions with a convenient syntax:

.. code:: django

    {% if perm in user|perms:object %} ... {% endif %}

The ``object`` argument is optional. If omitted, the global permission is checked,
similar to Django's `perms object`_.

.. _perms object:
    https://docs.djangoproject.com/en/1.9/topics/auth/default/#permissions

Examples:

.. code:: html+django


    {% if 'news.read_article' in user|perms:article %}
        {{ article.text }}
    {% else %}
        You do not have permission to read this article.
    {% endif %}


    {% if 'news.change_article' in user|perms:article %}
        <a href="...">Edit article</a>
    {% endif %}

    {% if 'news.delete_article' in user|perms:article %}
        <a href="...">Delete article</a>
    {% endif %}

The library provides ``can_change`` and ``can_delete`` shorthands for checking Django's default
``app.change_model`` and ``app.delete_model`` model permissions:

.. code:: html+django

    {% if user|can_change:article %} <a href="...">Edit</a> {% endif %}
    {% if user|can_delete:article %} <a href="...">Delete</a> {% endif %}


``BaseAuthorizationBackend``
----------------------------

This base class provides all the boilerplate code necessary for a Django `authentication backend`_
to work, without performing any user authentication or permission authorization itself.

This is intended to make it easy to write `custom authorization`_ policies that only implement the backend
methods they're interested in:

.. _authentication backend:
    https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#writing-an-authentication-backend

.. _custom authorization:
    https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#handling-authorization-in-custom-backends

.. code:: python

    from auth_utils.backends import BaseAuthorizationBackend


    class ArticleEditPolicy(BaseAuthorizationBackend):
        """
        Allow authors to change and delete their own articles.
        """

        def get_user_permissions(self, user_obj, obj=None):
            is_author = isinstance(obj, Article) and article.author == user_obj
            if user_obj.is_active and is_author:
                return {'news.change_article', 'news.delete_article'}
            else:
                return set()


    class GuestAccessPolicy(BaseAuthorizationBackend):
        """
        Allow anonymous users to read non-premium articles.
        """

        def get_user_permissions(self, user_obj, obj=None):
            guest_readable = isinstance(obj, Article) and not article.is_premium
            if not user_obj.is_authenticated() and guest_readable:
                return {'news.read_article'}
            else:
                return set()

Once defined, these policies can be enabled in AUTHENTICATION_BACKENDS_:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',

        # Custom authorization policies
        'news.auth.ArticleEditPolicy',
        'news.auth.GuestAccessPolicy',
    ]

.. _AUTHENTICATION_BACKENDS:
    https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-AUTHENTICATION_BACKENDS


Related work
============

Inspiration: `django-model-utils`_

`django-guardian`_ provides object-based permission checking utilities:

* View: An `alternative PermissionRequiredMixin`_, predating Django's one
* Template tag: `get_obj_perms`_, using somewhat clunkier assignment syntax


.. _django-model-utils: https://django-model-utils.readthedocs.org/

.. _django-guardian: http://django-guardian.readthedocs.org/
.. _alternative PermissionRequiredMixin:
    http://django-guardian.readthedocs.org/en/stable/api/guardian.mixins.html#permissionrequiredmixin
.. _get_obj_perms:
    http://django-guardian.readthedocs.org/en/stable/api/guardian.templatetags.guardian_tags.html#get-obj-perms
