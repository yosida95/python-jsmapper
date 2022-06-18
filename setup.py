# -*- coding: utf-8 -*-

import os
import sys

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)
requires = [
    'jsonschema==4.6.0',
]
if sys.version_info <= (3, 5):
    requires.append('zipp == 1.2.0')
tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-flake8',
]


def _read(name):
    return open(os.path.join(here, name)).read()


setup(
    name='jsmapper',
    version='0.1.9',
    description='A Object - JSON Schema Mapper.',
    long_description=_read("README.rst"),
    license='MIT',
    url='https://github.com/yosida95/python-jsmapper',

    author='Kohei YOSHIDA',
    author_email='kohei@yosida95.com',

    packages=find_packages(),
    python_requires='>= 3.5',
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
    },
    test_suite='jsmapper',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
