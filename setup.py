#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-tagging',
    version='1.3.3',
    description='Extensible tags in Django',
    author='Yigit Ozen',
    license='MIT',
    packages=[
        'tagging',
        'tagging.migrations',
        'tagging.management',
        'tagging.management.commands',
        ],
    requires=[
        'unicodecsv (>=0.9.4)'
    ],
    package_data={'tagging': ['templates/*']},
)
