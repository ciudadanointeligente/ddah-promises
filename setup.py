#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

file_dir = os.path.abspath(os.path.dirname(__file__))

with open('dependency_links.txt') as f:
    dependency_links = f.read().splitlines()
with open('requirements.txt') as f:
    reqs = f.read().splitlines()

def read_file(filename):
    filepath = os.path.join(file_dir, filename)
    return open(filepath).read()


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ddah-promises',
    version='0.0.8',
    packages=['promises', 'promises.csv_loader'],
    include_package_data=True,
    license='Affero',
    description='Promises app.',
    long_description=read_file('README.rst'),
    test_suite='runtests.runtests',
    url='http://github.com/ciudadanointeligente/ddah-promises',
    author=u'Felipe Álvarez / Juan Pablo Pérez Trabucco',
    author_email='lab@ciudadanointeligente.org',
    classifiers=[
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
    install_requires=reqs,
    dependency_links=dependency_links,
)
