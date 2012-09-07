.. _installation:

Installation
============

The quickest (and best) option for installing xbmcswift2 depends on Python 2.5
or higher, virtualenv and pip.

virtualenv
----------

Virtualenv is an awesome tool that enables clean installation and removal of
python libraries into a "virtual environment". Using a virtual environment
means that when you install a library, it doesn't pollute your system-wide
python installation. This makes it possible to install different versions of
library in different environments and they will never conflict.

If you already have pip installed, you can simply::

    $ sudo pip install virtualenv

or if you only have easy_install::

    $ sudo easy_install virtualenv

I also like to use some helpful virtualenv scripts, so install
virtualenv-wrapper::

    $ sudo pip install virtualenv-wrapper

Creating a Virtual Environment
------------------------------

Now we can create our virtualenv::

    $ mkvirtualenv xbmcswift2

When this completes, your prompt should now be preceded by `(xbmcswift2)`.
Now we install xbmcswift2::

    $ pip install xbmcswift2

Everything should be good to go. When you would like to work on your project
again, simply::

    $ workon xbmcswift2

and to deactive the virtualenv::

    $ deactivate
