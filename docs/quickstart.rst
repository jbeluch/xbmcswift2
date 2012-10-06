.. _quickstart:

Quickstart
============

If you haven't already installed xbmcswift2, head over to the `installation`
page.

The purpose of xbmcswift2 is to empower plugin writers to develop and debug
their plugins faster. This is faciliated by:

* A bootstrap script to create an empty addon complete with folder structure
  and required files.

* Seamless testing of addons by enabling an addon to be run on the command line
  or in XBMC. xbmcswift2 handles mocking the xbmc python modules to ensure your
  addon will run (in a limited fashion) outside of XBMC *without* any code
  changes.

* Basic URL routing code, so you can focus on writing the web parsing code
  specific to your plugin, and not deal with repeated boilerplate and url
  parsing.

* A library of helpful functions and code patterns to enhance your addon's
  functionality.


Introduction to XBMC Addons
---------------------------

Before going any further, you should already be familiar with the general file
structure and necessary files for an XBMC addon. If not, please spend a few
minutes reading about addons in the XBMC wiki_.

.. _wiki: http://wiki.xbmc.org/index.php?title=Add-on_development


Creating the Plugin Skeleton
----------------------------

xbmcswift2 comes with a helpful console script that will create a plugin
skeleton for you, including all the necessary folders and files to get started.
Simply run `xbmcswift2 create` and answer a few questions to personalize your
addon.

Below is an example session::

    $ xbmcswift2 create

        xbmcswift2 - A micro-framework for creating XBMC plugins.
        xbmc@jonathanbeluch.com
        --

    I'm going to ask you a few questions to get this project started.
    What is your plugin name? : Hello XBMC
    Enter your plugin id. [plugin.video.helloxbmc]:
    Enter parent folder (where to create project) [/private/tmp]: 
    Enter provider name : Jonathan Beluch (jbel)
    Projects successfully created in /private/tmp/plugin.video.helloxbmc.
    Done.


Hello XBMC
----------

If you navigate to the newly created folder ``plugin.video.helloxbmc``, you'll
find an ``addon.py`` exactly like the one below.

.. sourcecode:: python

    from xbmcswift2 import Plugin


    plugin = Plugin()


    @plugin.route('/')
    def index():
        item = {
            'label': 'Hello XBMC!',
            'path': 'http://s3.amazonaws.com/KA-youtube-converted/JwO_25S_eWE.mp4/JwO_25S_eWE.mp4',
            'is_playable': True
        }
        return [item]


    if __name__ == '__main__':
        plugin.run()

The above code is a fully functioning XBMC addon (not that it does much!). So
what does the code do?

1. After importing the Plugin class, we create our plugin instance. xbmcswift
   will parse the proper addon name and id from the addon.xml file.

2. We are using the ``plugin.route`` decorator on the ``index`` function. This
   binds a url path of '/' to the index function. ('/' is the default URL
   path).

   Note: The url rule of '/' must always exist in a plugin. This is the default
   route when a plugin is first run.

3. The index function creates a single dict with some key/vals. This is how you
   create a listitem using xbmcswift2. At a minimum, most items have a ``path``
   and ``label``. The ``is_playable`` flag tells XBMC that this is a media
   item, and not a URL which points back to an addon.

4. We return a list from the index function, that contains a single item. For a
   typical xbmcswift2 view, this is the proper way to add list items.

5. We call ``plugin.run()`` to run our plugin. It is imperative that this line
   is inside the ``__name__`` guard. If it is not, your addon won't run
   correctly on the command line.


Running Addons from the Command Line
------------------------------------

One of the shining points of xbmcswift2 is the ability to run plugins from the
command line. To do so, ensure your working directory is the root of your addon
folder (where you addon.xml file is located) and execute ``xbmcswift2 run``.::

    $ xbmcswift2 run
    2012-05-02 19:02:37,785 - DEBUG - [xbmcswift2] Adding url rule "/" named "index" pointing to function "index"
    2012-05-02 19:02:37,798 - DEBUG - [xbmcswift2] Dispatching / to once
    2012-05-02 19:02:37,798 - INFO - [xbmcswift2] Request for "/" matches rule for function "index"
    ----------------------
     #  Label       Path
    ----------------------
    [0] Hello XBMC! (None)
    ----------------------

Right away we can see the output of our plugin. When running in the CLI,
xbmcswift2 prints log messages to STDERR, so you can hide them by appending
``2>/dev/null`` to the previous command.. Below the logs we can see a simple
display of our listitems, in this case a single item.

See :ref:`commandline` for a more detailed explanation of running on the command line.


URL Routing
-----------

Another advantage of using xbmcswift2, is its clean URL routing code. This
means you don't have to write your own code to parse the URL provided by XBMC
and route it to a specific function. xbmcswift2 uses a a path passed to the
:meth:`~xbmcswift2.Plugin.route` decorator to bind a URL to a function. For
example, a route of ``/videos/`` will result in a URL of
``plugin://plugin.video.helloxbmc/videos/`` calling the decorated function.

It's even possible to pass variables to functions from the URLs. You might
have a function like this to list videos for a given category:

.. sourcecode:: python

    @plugin.route('/categories/<category>/')
    def show_videos(category):
        '''Display videos for the provided category'''
        # An incoming URL of /categories/science/ would call this function and
        # category would have a value of 'science'.
        items = get_video_items(category)
        return plugin.finish(items)

Currently, there is no type coercion, so all variables plucked from URLs will
be strings.

Now we have a way of directing incoming URLs to specific views. But how do we
link list items to other views in our code? We'll modify our Hello XBMC addon:

.. sourcecode:: python

    @plugin.route('/')
    def index():
        items = [
            {'label': 'Hola XBMC!', 'path': plugin.url_for('show_label', label='spanish')},
            {'label': 'Bonjour XBMC!', 'path': plugin.url_for('show_label', label='french')},
        ]
        return items


    @plugin.route('/labels/<label>/')
    def show_label(label):
        # Normally we would use label to parse a specific web page, in this case we are just
        # using it for a new list item label to show how URL parsing works.
        items = [
            {'label': label},
        ]
        return items

Let's run our plugin interactively now to explore::

    $ xbmcswift2 run interactive
    2012-05-02 19:14:53,792 - DEBUG - [xbmcswift2] Adding url rule "/" named "index" pointing to function "index"
    2012-05-02 19:14:53,792 - DEBUG - [xbmcswift2] Adding url rule "/labels/<label>/" named "show_label" pointing to function "show_label"
    2012-05-02 19:14:53,793 - DEBUG - [xbmcswift2] Dispatching / to interactive
    2012-05-02 19:14:53,794 - INFO - [xbmcswift2] Request for "/" matches rule for function "index"
    -------------------------------------------------------------------
     #  Label         Path
    -------------------------------------------------------------------
    [0] Hola XBMC!    (plugin://plugin.video.helloxbmc/labels/spanish/)
    [1] Bonjour XBMC! (plugin://plugin.video.helloxbmc/labels/french/)
    -------------------------------------------------------------------
    Choose an item or "q" to quit: 0

    2012-05-02 19:14:59,854 - INFO - [xbmcswift2] Request for "/labels/spanish/" matches rule for function "show_label"
    ----------------------------------------------
    #  Label   Path
    ----------------------------------------------
    [0] ..      (plugin://plugin.video.helloxbmc/)
    [1] spanish (None)
    ----------------------------------------------
    Choose an item or "q" to quit: q

    $ python addon.py interactive
    --
    [0] Hola XBMC! (plugin://plugin.video.helloxbmc/labels/spanish/)
    [1] Bonjour XBMC! (plugin://plugin.video.helloxbmc/labels/french/)
    Choose an item or "q" to quit: 0
    --
    [0] spanish (None)

We've introduced a few new topics here.

* We passed ``interactive`` as a positional argument to the ``xbmcswift2 run``
  command. This enables us to interact with the list items rather than just
  print them once and exit.

* We've used :meth:`~xbmcswift2.Plugin.url_for` to create a url pointing to a
  different view function. This is how view functions create list items that
  link to other functions.

* Our function ``show_label`` requires an argument 'label', so we pass a
  keyword argument with the same name to url_for.

* To set the url for a list item, we set the 'path' keyword in the item
  dictionary.

* xbmcswift2 display a list item of '..', which is simliar to XBMC's '..' list
  item. This enables you to go back to the parent directory.

To learn more about URL routing and other available options, check out the <API>
or the <patterns page>.


Playing Media
-------------

The last thing we haven't covered is how to play an actual video. By default,
all items returned are directory items. This means that they act as a directory
for more list items, and its URL points back into the plugin. To differentiate
playable media from directory items, we set ``is_playable`` to ``True`` in our
item dictionary.

First, let's add a new view to play some media:

.. sourcecode:: python

    @plugin.route('/videos/')
    def show_videos():
        items = [
            {'label': 'Calculus: Derivatives 1',
             'path': 'http://s3.amazonaws.com/KA-youtube-converted/ANyVpMS3HL4.mp4/ANyVpMS3HL4.mp4',
             'is_playable': True,
             }
        ]
        return plugin.finish(items)

As you can see, the URL value for *path* is a direct link to a video asset, we are not calling
``url_for``. If you need to use XBMC's ``setResolveUrl`` functionality, see the
patterns section for ``plugin.set_resolved_url``.

Now let's update out item dictionary in show_label to add a path:

.. sourcecode:: python

            {'label': label, 'path': plugin.url_for('show_videos')},

Now, you have a fully functioning XBMC addon, complete with nested menus and
playable media.

One more section before going off on your own!


Using xbmc, xbmcgui, xbmcaddon
------------------------------

You can always import and call any of the xbmc modules directly if you need
advanced functionality that xbmcswift2 doesn't support. However, if you still
want the ability to run plugins from the command line you should import the
xbmc modules from xbmcswift2.

.. sourcecode:: python

   from xbmcswift2 import xbmc, xbmcgui

Since these modules are written in C, they are only available when running
XBMC. To enable plugins to run on the command line, xbmcswift2 has mock
versions of these modules.


Going further
-------------
 
This should be enough to get started with your first simple XBMC addon. If
you'd like more information, please check out the detailed :ref:`tutorial` and
also review common :ref:`patterns`.
