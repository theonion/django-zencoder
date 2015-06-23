#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


name = "django-zencoder"
package = "zencoder"
description = "A Django app that allows the upload and encoding of videos with Zencoder"
url = "https://github.com/theonion/django-zencoder"
author = "Onion Tech Team"
author_email = "tech@theonion.com"
license = "MIT"
requires = [
    "Django>=1.8",
    "requests==2.2.1",
    "django-json-field==0.5.5",
    "six==1.5.2",
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, "__init__.py"))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, "", 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, "__init__.py"))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages("zencoder"),
    package_data=get_package_data(package),
    install_requires=requires,
    tests_require=["httmock==1.2.2", "pytest==2.7.1", "pytest-django==2.8", "coveralls==0.4.1", "pytest-cov==1.6"],
)
