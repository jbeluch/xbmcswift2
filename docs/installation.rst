.. _installation:

Installation
============

.. note::

    The purpose of xbmcswift2 is to have the ability to run the addon on the
    command line as well as in XBMC. This means that we will have to install
    xbmcswift2 twice, once for the command line and once as an XBMC addon.


The easiest way to get the most recent version of xbmcswift2 for XBMC is to
install an addon that requires xbmcswift2. You can find a list of such addons
on the :ref:`poweredby` page. The other options is download the correct version
from https://github.com/jbeluch/xbmcswift2-xbmc-dist/tags and unpack it into
your addons folder.  

Now, on to installing xbmcswift2 for use on the command line.

virtualenv
----------

Virtualenv is an awesome tool that enables clean installation and removal of
python libraries into a "virtual environment". Using a virtual environment
means that when you install a library, it doesn't pollute your system-wide
python installation. This makes it possible to install different versions of a
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
