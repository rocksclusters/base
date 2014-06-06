#!/opt/rocks/bin/python
#
#

from distutils.core import setup
from setuptools import find_packages
import os

version = os.environ.get('ROCKS_VERSION')

# 
# main configuration of distutils
# 
setup(
    name = 'rocks-pylib',
    version = version,
    description = 'Main Rocks python library',
    author = 'Phil Papadopoulos',
    author_email =  'philip.papadopoulos@gmail.com',
    maintainer = 'Luca Clementi',
    maintainer_email =  'luca.clementi@gmail.com',
    platforms = ['linux'],
    url = 'https://rocksclusters.org',
    #long_description = long_description,
    #license = license,
    #main package, most of the code is inside here
    packages = find_packages(),
    #data_files = [('etc', ['etc/rocksrc'])],
    # disable zip installation
    zip_safe = False,
    #the command line called by users    
    scripts=['bin/rocks'],
)
