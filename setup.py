#!/usr/bin/env python
"""
Copyright (c) 2016-2019 Joshua W
"""


version = '0.4.1'

from setuptools import setup
setup(name='psv',
      install_requires=["tabulate==0.8.10"],
      version=version,
      description='CSV Parser',
      long_description="""PSV
----

PSV is a library that allows rapid script development for csv files. This library allows pythonic manipulation of csv (or csv like structures).

This is not a data analysis library rather a data manipulation one, and it is meant to be as light as possbile. For these usecases, consider Pandas. Additionally, CSV files should not be used as any sort of flat file database and this library doesn't actively support that usecase.
""",
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
