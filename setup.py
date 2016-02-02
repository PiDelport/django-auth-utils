from setuptools import setup, find_packages

setup(
    name='django-auth-utils',
    use_vcs_version=True,

    author='Piet Delport',
    author_email='pjdelport@gmail.com',

    package_dir={'': 'src'},
    packages=find_packages('src'),

    setuptools_requires=['setuptools_scm'],

    install_requires=[
        'attrs',
        'Django',
    ],

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
