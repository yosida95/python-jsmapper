# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

here = os.path.dirname(__file__)
requires = [
    'jsonschema==2.4.0',
]
tests_require = [
    'nose',
    'coverage'
]


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except:
        return ""
readme = _read("README.rst")
license = _read("LICENSE.rst")

setup(
    name='jsmapper',
    version='0.1.9',
    test_suite='jsmapper',
    author='Kohei YOSHIDA',
    author_email='license@yosida95.com',
    description='A Object - JSON Schema Mapper.',
    long_description=readme,
    license=license,
    url='https://github.com/yosida95/python-jsmapper',
    packages=find_packages(),
    install_requires=requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
