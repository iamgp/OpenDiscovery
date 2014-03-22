#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import OpenDiscovery as od

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='OpenDiscovery',
    version=od.__version__,
    release='0',
    description='Computational Drug Discovery Software',
    long_description=read('README.rst'),
    author='Gareth Price',
    author_email='gareth.price@warwick.ac.uk',
    maintainer='Gareth Price',
    maintainer_email='gareth.price@warwick.ac.uk',
    url='https://github.com/iamgp/OpenDiscovery',
    packages=['OpenDiscovery', 'OpenDiscovery.pyPDB'],
    package_dir={'OpenDiscovery': 'OpenDiscovery'},
    package_data={'OpenDiscovery': ['lib/vina-osx/*', 'lib/vina-linux/*', 'lib/*.aw']},
    include_package_data=True,
    install_requires=['matplotlib>=1.4', 'pandas>0.13'],
    license="GPL",
    keywords='OpenDiscovery',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry'
    ],
    scripts=['odscreen.py', 'odmscreen.py']
)