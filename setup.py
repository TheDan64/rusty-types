#! /usr/bin/env python

from setuptools import setup, find_packages

requires = [

]

tests_require = [
    "pytest",
]

setup(name="rustytypes",
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
