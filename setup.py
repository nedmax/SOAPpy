#!/usr/bin/env python

CVS=0

from setuptools import setup, find_packages
import os

def read(*rnames):
    return "\n"+ open(
        os.path.join('.', *rnames)
    ).read()
url="https://github.com/nedmax/SOAPpy.git"
long_description="SOAPpy provides tools for building SOAP clients and servers.  For more information see " + url\
    +'\n'+read('README.md')\
    +'\n'+read('CHANGES.md')
setup(
    name="SOAPpy",
    version='0.12.24',
    description="SOAP Services for Python",
    maintainer="Gregory Warnes, kiorky",
    maintainer_email="Gregory.R.Warnes@Pfizer.com, kiorky@cryptelium.net",
    url = url,
    long_description=long_description,
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    install_requires=[
        'wstools',
        'defusedxml',
        'requests'
    ]
)
