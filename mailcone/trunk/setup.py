from setuptools import setup, find_packages

version = '1.0'

setup(name='mailFilter',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'grokui.admin',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.startup',
                        # Add extra requirements here
                        'zc.catalog',
                        'hurry.query',
                        'megrok.resource',
                        'js.jquery',
                        'js.jqueryui',
                        'zope.pluggableauth',
                        'megrok.rdb', # used for mails
                        ],
      entry_points={
          'fanstatic.libraries': [
              'mailfilter = mailfilter.resource:library',
          ]
      })
