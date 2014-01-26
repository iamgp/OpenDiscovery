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

setup(
    name='OpenDiscovery',
    version=od.__version__,
    release='0',
    description='Computational Drug Discovery Software',
    long_description='Open Discovery is a suite of programs that use Open Source or freely available tools to dock a library of chemical compounds against a receptor protein. In a (currently submitted) paper in the Journal ofChemical Education, we outline the usefulness of having anuncomplicated, free-to-use protocol to accomplish a task that has beenthe subject of academic and commercial interest for decades. We alsohighlight the gaps in open source tools around preparing protein -ligand complexes for molecular simulation, an area we expect to developin the future.',
    author='Gareth Price',
    author_email='gareth.price@warwick.ac.uk',
    url='https://github.com/iamgp/OpenDiscovery',
    packages=['OpenDiscovery', 'OpenDiscovery.pyPDB'],
    package_dir={'OpenDiscovery': 'OpenDiscovery'},
    package_data={'OpenDiscovery': ['lib/vina-osx/*', 'lib/vina-linux/*', 'lib/*.aw']},
    include_package_data=True,
    install_requires=[],
    license="GPL",
    keywords='OpenDiscovery',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    scripts=['odscreen.py']
)