# coding: utf-8
from setuptools import setup, find_packages


def README():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-auth-utils',
    description='Django authentication and authorization utilities',
    long_description=README(),
    url='https://github.com/pjdelport/django-auth-utils',

    author='Pi Delport',
    author_email='pjdelport@gmail.com',

    package_dir={'': 'src'},
    packages=find_packages('src'),

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    install_requires=[
        'attrs',
        'Django',
    ],

    license='Public Domain',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
