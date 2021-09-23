#!/usr/bin/env python3

""" Setup file
"""
import sys
from setuptools import setup, find_packages
from pkg_resources import VersionConflict, require

import mc_mod_getter

try:
    require('setuptools>=38.3')
except VersionConflict:
    print('Error: Update setuptools')
    sys.exit(1)


if __name__ == '__main__':
    setup(
        name=mc_mod_getter.__title__,
        version=mc_mod_getter.__version__,
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=['tests']),
        install_requires=['PyYAML','requests','urllib3','click'],
        include_package_data=True,
        zip_safe=False,
        author=mc_mod_getter.__author__,
        author_email=mc_mod_getter.__author_email__,
        description=mc_mod_getter.__description__,
        license=mc_mod_getter.__license__,
        keywords=mc_mod_getter.__keywords__,
        url=mc_mod_getter.__url__,
        project_urls=mc_mod_getter.__project_urls__,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.9',
            'Natural Language :: English'
        ]
    )
