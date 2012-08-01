from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='raptus.mailcone.layout',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Samuel Riolo',
      author_email='sriolo@raptus.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raptus','raptus.mailcone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'grokcore.chameleon',
          'grokcore.layout',
          'fanstatic',
          'zope.fanstatic',
          'js.jquery',
          'js.jqueryui',
          'js.jquery_datatables',
          'js.jquery_elastic',
          'js.jquery_splitter',
          'js.jquery_cookie',
          'js.jquery_jqtransform',
          'js.codemirror',
          'js.jquery_caret',
          'js.jquery_ba_resize',
          'horae.js.jqplot',
          'megrok.navigation',
          'megrok.form',
          'megrok.rendersource',
          'zope.app.renderer',
          'horae.datetime',
          

      ],
      entry_points={
          'fanstatic.libraries': [
              'raptus.mailcone.layout = raptus.mailcone.layout.resource:library',
          ]
      })
