#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

from registration_names import VERSION


# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

NAME = "django-registration_names"

DESCRIPTION = "A way to control allowed and prohibited user names for registration with django-registration."
LONG_DESCRIPTION = DESCRIPTION

AUTHOR = "Ivan Yurchenko <ivan0yurchenko@gmail.com>"
AUTHOR_EMAIL = "ivan0yurchenko@gmail.com"

MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL

URL = 'https://github.com/ivanyu/django-registration-names'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords="django, views, forms, mixins",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    license="MIT License",
    packages=["registration"],
    zip_safe=False,
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
