'''

xbmcswift2
~~~~~~~~~~

A micro framework to enable rapid development of XBMC plugins.


Features
````````

* Run the addon from the command line *or* within XBMC without changing any
  code.
* Helper libraries to make common XBMC api operations easy, like adding items,
  getting settings, creating temporary files, etc.
* Handles all the url parsing involved in plugin routing. No need to deal with
  complicated URLs and query strings.


Documentation
`````````````

The current documentation can be found at http://www.xbmcswift.com

Development
```````````

This module is now available in the official XBMC Eden repository as
xbmcswift2.

This project is the next version of xbmcswift. While the APIs are similar,
there are a few things that are not backwards compatible with the original
version, hence the new name.


Contact
```````

https://github.com/jbeluch/xbmcswift2

xbmc@jonathanbeluch.com
'''
import os
from setuptools import setup, find_packages


setup(
    name = 'xbmcswift2',
    version = '0.1.1',
    author = 'Jonathan Beluch',
    author_email = 'web@jonathanbeluch.com',
    description = 'A micro framework for rapid development of XBMC plugins.',
    license = "GPL3",
    keywords = "example documentation tutorial",
    url = 'https://github.com/jbeluch/xbmcswift2',
    packages=find_packages(),
    include_package_data=True,
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
    ],
    entry_points={
       'console_scripts': [
           'xbmcswift2 = xbmcswift2.cli.cli:main',
       ]
    },
)
