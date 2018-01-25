#!/usr/bin/env python

from setuptools import setup, find_packages
import sys
#import orionxapi

long_desc = '''Orionx API Client for Python is a client 
library to manage operations on the Orionx exchange platform.'''

install_requires = [
  'requests==2.18.4',
  'six==1.11.0',
  'ujson==1.35',
  'graphql-core==2.0',
  'pygql==0.1.4',
  'fake-useragent==0.1.8'
]

if sys.version_info < (3, 5):
    install_requires.append('futures')

version = '1.0.5'

setup(name='orionx-api-client',
  version=version,
  description='Orionx API Client',
  long_description=long_desc,
  url='http://github.com/itolosa/orionx-api-client',
  author='Ignacio Tolosa Guerrero',
  author_email='ignacio@perejil.cl',
  maintainer='Ignacio Tolosa Guerrero',
  maintainer_email='ignacio@perejil.cl',
  license='MIT',
  keywords='orionx api client',
  packages=find_packages(exclude=['tests', 'examples']),
  zip_safe=False,
  install_requires=install_requires,
  package_data={},
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP'
])