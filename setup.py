import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'xbmcswift2',
    version = '0.1-dev',
    author = 'Jonathan Beluch',
    author_email = 'web@jonathanbeluch.com',
    description = 'A micro framework for rapid development of XBMC plugins.',
    license = "GPL3",
    keywords = "example documentation tutorial",
    #url = '',
    #packages=['xbmcswift'],
    #package_dir={'xbmcswift': 'xbmcswift'},
    package_data={'xbmcswift2': [
        #skel/
        'cli/data/addon.xml',
        'cli/data/addon.py',
        #'skel/resources',
        #'skel/resources/lib',
        'cli/data/resources/lib/__init__.py',
        'cli/data/resources/__init__.py',
        #'skel/resources/language',
        #'skel/resources/language/English',
        'cli/data/resources/language/English/strings.xml',
    ]},

    packages=find_packages(),
    #packages=['xbmcswift2'],
    include_package_data=True,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        #"License :: OSI Approved :: BSD License",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
    ],
    entry_points={
       'console_scripts': [
           'xbmcswift2 = xbmcswift2.cli.cli:main',
       ]
    },
)
