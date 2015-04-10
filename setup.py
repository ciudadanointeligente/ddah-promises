#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'ddah-promises',
    version = '0.1',
    packages = ['promises'],
    include_package_data = True,
    license = 'Affero',
    description = 'Promises app.',
    long_description = README,
    test_suite = 'runtests.runtests',
    url = 'http://github.com/ciudadanointeligente/ddah-promises',
    author = u'Felipe Álvarez / Juan Pablo Pérez Trabucco',
    author_email = 'lab@ciudadanointeligente.org',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
	'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    install_requires =[
        'django-taggit',
        'django-popolo',
    ],
    dependency_links =[
        'http://github.com/openpolis/django-popolo/tarball/master#egg=django-popolo'
    ],
)
