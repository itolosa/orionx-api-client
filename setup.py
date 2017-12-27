#!/usr/bin/env python

from setuptools import setup

import orionxapi

long_desc = '''Orionx API Client for Python is a client 
library to manage operations on the Orionx exchange platform.'''

install_requires = [
  'requests==2.18.4',
  'six==1.11.0',
  'ujson==1.35'
]

version = orionxapi.__version__

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
  packages=['orionxapi'],
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