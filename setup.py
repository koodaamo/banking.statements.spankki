from setuptools import setup, find_packages
import os

version = '0.1dev0'

setup(name='banking.statements.spankki',
      version=version,
      description="Account statement reader plugin for S-Pankki of Finland",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Utilities',
        'Environment :: Console',
        'Operating System :: OS Independent',
        ],
      keywords=['ofxstatement','ofx'],
      author='Petri Savolainen',
      author_email='petri.savolainen@koodaamo.fi',
      url='https://github.com/koodaamo/banking.statements.spankki',
      license='GPLv3',
      namespace_packages = ['banking', 'banking.statements'],
      packages = ['banking.statements.spankki'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'ofxstatement'
      ],
      entry_points="""
          [ofxstatement]
          op = banking.statements.spankki.plugin:SPPlugin
      """
      )
