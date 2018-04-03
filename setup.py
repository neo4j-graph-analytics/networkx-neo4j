#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for networkx
You can install networkx with
python setup.py install
"""
from glob import glob
import os
import sys
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (3, 6):
    print("NetworkX Neo4j requires Python 3.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Write the version information.
sys.path.insert(0, 'networkx-neo4j')
import release
version = release.write_versionfile()
sys.path.pop(0)

packages = ["nxneo4j"]

docdirbase = 'share/doc/networkx-neo4j-%s' % version
# add basic documentation
data = [(docdirbase, glob("*.txt"))]
# add examples


if __name__ == "__main__":

    setup(
        name=release.name.lower(),
        version=version,
        maintainer=release.maintainer,
        maintainer_email=release.maintainer_email,
        author=release.authors['Hagberg'][0],
        author_email=release.authors['Hagberg'][1],
        description=release.description,
        keywords=release.keywords,
        long_description=release.long_description,
        license=release.license,
        platforms=release.platforms,
        url=release.url,
        download_url=release.download_url,
        classifiers=release.classifiers,
        packages=packages,
        data_files=data,
        test_suite='nose.collector',
        tests_require=['nose>=0.10.1'],
        zip_safe=False
    )