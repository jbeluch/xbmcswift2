xbmcswift2
==========

[![Build Status](https://secure.travis-ci.org/jbeluch/xbmcswift2.png)](http://travis-ci.org/jbeluch/xbmcswift2)

A micro framework to enable rapid development of XBMC plugins.


## Features
* Run the addon from the command line *or* within XBMC without changing any
  code.
* Helper libraries to make common XBMC api operations easy, like adding items,
  getting settings, creating temporary files, etc.
* Handles all the url parsing involved in plugin routing. No need to deal with
  complicated URLs and query strings.

## Installation

xbmcswift2 is available in pypi, so you can install via pip:

    pip install xbmcswift2

You should probably also read
http://www.xbmcswift.com/en/latest/installation.html#installation to ensure it
is properly installed for XBMC as well.

## Documentation

The current documentation can be found at http://www.xbmcswift.com. It covers
installation, quickstart, a guide to writing an addon and documentation for the
full xbmcswift2 API.

## Upgrading from xbmcswift

This project is the next version of xbmcswift. While the APIs are similar,
there are a few things that are not backwards compatible with the original
version, hence the new name.

If you are upgrading an addon that used xbmcswift, see
http://www.xbmcswift.com/en/latest/upgrading.html#upgrading.

## Development

xbmcswift2 is now available in the official XBMC Eden repository. Every time a
new release is created and uploaded to pypi, a new XBMC release will be created
as well. Be aware that XBMC's "version" for xbmcswift2 will not match the
official python package version.

New features and bug fixes are done on the develop branch of this repo. If you
are interested in using the develop branch, you can install locally via pip:

    pip install git+git://github.com/jbeluch/xbmcswift2.git@develop

The documentation for the develop branch can be found at
http://www.xbmcswift.com/en/develop/api.html#api.

## Contributing

Bugs, patches and suggestions are all welcome. I'm working on adding tests and
getting better coverage. Please ensure that your patches include tests as well
as updates to the documentation. Thanks!

## Support

\#xbmcswift on freenode

https://github.com/jbeluch/xbmcswift2

web@jonathanbeluch.com
