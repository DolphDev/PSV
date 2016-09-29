#!/usr/bin/env python
"""

 _______    ___   .___________.    _______.___________.    ___      ___   ___ 
|   ____|  /   \  |           |   /       |           |   /   \     \  \ /  / 
|  |__    /  ^  \ `---|  |----`  |   (----`---|  |----`  /  ^  \     \  V  /  
|   __|  /  /_\  \    |  |        \   \       |  |      /  /_\  \     >   <   
|  |    /  _____  \   |  |    .----)   |      |  |     /  _____  \   /  .  \  
|__|   /__/     \__\  |__|    |_______/       |__|    /__/     \__\ /__/ \__\ 
                                                                              

Copyright (c) 2016 FatStax.
"""


version = '0.0.1.6'

from setuptools import setup
setup(name='psv',
      install_requires=[],
      version=version,
      description='CSV Parser',
      author='Joshua Walters',
      author_email='joshua.walters@fatstax.com',
      url='https://github.com/RedFunnel/PSV',
      packages=['psv', 'psv.core', 'psv.core.objects', 'psv.core.parsing', 'psv.core.output', "psv.core.utils", "psv.core.exceptions"],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      keywords=['csv', "Comma Separated Values", "Python Separated Values"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5"]      )
