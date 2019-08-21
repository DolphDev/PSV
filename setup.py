#!/usr/bin/env python
"""
Copyright (c) 2016-2019 Joshua W
"""

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readmeshort.md'), encoding='utf-8') as f:
    long_description = f.read()


version = '0.4.0'

from setuptools import setup
setup(name='psv',
      install_requires=["tabulate==0.8.3"],
      version=version,
      description='CSV Parser',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Joshua W',
      author_email='DolphDevgithub@gmail.com',
      url='https://github.com/DolphDev/PSV',
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
