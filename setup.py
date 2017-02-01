#! /usr/bin/env python

from setuptools import setup, find_packages
from sys import version_info

requires = []

major, minor, micro, _, _ = version_info

assert major == 3, "Rusty types is only supported in Python 3"

if minor < 5:
    requires.append("typing>=3.5.3")
elif minor == 5 and micro < 3:
    assert micro < 3, "Rusty types requires Python 3.5 micro version 3 or higher"

tests_require = [
    "pytest",
]

setup(name="rusty_types",
      version="0.1.0pre",
      description="",
      long_description="",
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
      ],
      author="Daniel Kolsoi",
      author_email="thadan64@gmail.com",
      url="https://github.com/TheDan64/rusty-types",
      packages=find_packages(),
      keywords=["rust"],
      include_package_data=True,
      test_suite="tests",
      tests_require=tests_require,
      install_requires=requires)
