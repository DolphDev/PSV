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


version = '0.0.1.5'

from setuptools import setup
setup(name='fatstax',
      install_requires=["openpyxl"],
      version=version,
      description='CSV Parser',
      author='Joshua Walters',
      author_email='joshua.walters@fatstax.com',
      url='https://github.com/Dolphman/pynationstates',
      packages=['fatstax', 'fatstax.core', 'fatstax.core.objects', 'fatstax.core.parsing', 'fatstax.core.output'],
      package_data={'': ['LICENSE.txt', "readme.md"]},
      keywords=['csv abstraction'],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.0",
                   "Programming Language :: Python :: 3.1",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5"]      )
