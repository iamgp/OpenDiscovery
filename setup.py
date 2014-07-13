#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import OpenDiscovery as od

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='OpenDiscovery',
    version=od.__version__,
    description='Computational Drug Discovery Software',
    long_description=read('README.rst'),
    author='Gareth Price',
    author_email='gareth.price@warwick.ac.uk',
    maintainer='Gareth Price',
    maintainer_email='gareth.price@warwick.ac.uk',
    url='https://github.com/iamgp/OpenDiscovery',
    packages=['OpenDiscovery'],
    package_dir={'OpenDiscovery': 'OpenDiscovery'},
    package_data={'OpenDiscovery': ['lib/vina-osx/vina', 'lib/vina-linux/vina', 'lib/extract.awk']},
    include_package_data=True,
    install_requires=['argparse','matplotlib', 'pandas', 'numpy', 'termcolor', 'docopt'],
    license="GPL",
    keywords='OpenDiscovery',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry'
    ],
    entry_points={
        'console_scripts': [
            'odscreen = OpenDiscovery.screen:cli'
        ],
    },
    zip_safe=False
)