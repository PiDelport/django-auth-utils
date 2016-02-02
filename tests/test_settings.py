"""
Stub settings for tests.
"""

SECRET_KEY = 'django-auth-utils tests'

ROOT_URLCONF = 'test_urls'


# Explicit default value, to silence system check warning 1_7.W001 in Django 1.8.
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
