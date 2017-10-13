"""
Stub settings for tests.
"""

SECRET_KEY = 'django-auth-utils tests'

ROOT_URLCONF = 'stub_urls'


# Explicit default value, to silence system check warning 1_7.W001 in Django 1.8.
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


INSTALLED_APPS = [
    'auth_utils',

    # These are needed for django.contrib.auth.mixins.PermissionRequiredMixin
    # to be importable by auth_utils.views.
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    },
]
