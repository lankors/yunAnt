#!/usr/bin/env python
#coding=utf-8

from setuptools import setup, find_packages


import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

import sys

if sys.version_info < (2, 6):
    sys.exit('Python 2.5 or greater is required.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as fp:
    readme = fp.read()

with open('LICENSE') as fp:
    license = fp.read()


setup(

    name = 'yunAnt',
    version = '1.3.0',
    keywords = ('yunAnt', 'aliyun','amazon','ucloud','qcloud','qingcloud'),
    description = 'rebot aliyun、amazon、ucloud、qcloud、qingcloud Cloud server information',
    long_description = readme,
    license=license,
    url = 'https://github.com/djshell/yunAnt',
    author = 'wqc2008@gmail.com',
    author_email = 'wqc2008@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['qingcloud-sdk','boto','requests'],
)
