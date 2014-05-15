# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import dtf
version = dtf.__version__

setup(
    name='d2f',
    version=version,
    author='',
    author_email='will@django.nu',
    packages=[
        'dtf',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['dtf/manage.py'],
)