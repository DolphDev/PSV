#!/usr/bin/env python
"""
Copyright (c) 2016, 2017, 2018 Joshua Walters
"""


version = '0.1.0'

from setuptools import setup
setup(name='psv',
      install_requires=["tabulate"],
      version=version,
      description='CSV Parser',
      author='Joshua W',
      author_email='DolphDevgithub@gmail.com',
      url='https://github.com/Dolphman/PSV',
      packages=['psv', 'psv.core', 'psv.core.objects', 'psv.core.parsing', 'psv.core.output', "psv.core.utils", "psv.core.exceptions"],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      keywords=['csv', "Comma Separated Values", "Python Separated Values", "psv"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6"]
                    )
