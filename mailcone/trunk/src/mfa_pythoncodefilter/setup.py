from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='mfa_pythoncodefilter',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'mailfilter',
          'zope.fanstatic',
          'zc.sourcefactory',
          #'mailgrokker',
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'fanstatic.libraries': [
              'mfa_pythoncodefilter = mfa_pythoncodefilter.resource:library',
          ]})
