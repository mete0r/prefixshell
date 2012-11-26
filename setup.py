# -*- coding: utf-8 -*-
import os
import os.path
cwd = os.getcwd()
setupdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(setupdir)
try:
    from setuptools import setup, find_packages
    setup(name='prefixshell',
          packages=find_packages(),
          entry_points = {
              'console_scripts': [
                  'prefix = prefixshell:main',
                  'panout = prefixshell.panout:main',
                  ],
              })
finally:
    os.chdir(cwd)
