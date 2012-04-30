.. _quickstart:

Quickstart
============

If you haven't already installed xbmcswift, head over to the `installation`
page.

The purpose of xbmcswift is to enable rapid plugin creation. This is faciliated
by:

* A bootstrap script to create an empty addon complete with folder structure
  and required files.

* Seamless testing of addons by enabling an addon to be run on the command line
  or in XBMC. xbmcswift handles mocking the xbmc python modules to ensure your
  addon will run (in a limited fashion) outside of XBMC>

* Basic URL routing code, so you can focus on writing the web parsing code
  specific to your plugin, and not deal with repeated boilerplate.

* A library of helpful functions and code patterns to enchance your addon's
  functionality.

Intro to XBMC addons
--------------------

Before going any further, you should already be familiar with the general file
structure and necessary files for an XBMC addon. If not, please spend a few minutes
reading about addons in the wiki_.

.. _wiki: http://wiki.xbmc.org/index.php?title=Add-on_development


Creating the Plugin Skeleton
----------------------------

xbmcswift comes with a helpful console script that will create a plugin
skeleton for you, including all the necessary folders and files to get started.
Simply run `xbmcswift create` and answer a few questions to personalize your
addon.

Below is an example session::

    $ xbmcswift create

        XBMC Swift - A micro-framework for creating XBMC plugins.
        xbmc@jonathanbeluch.com
        --

        I'm going to ask you a few questions to get this project started.
        What is your plugin name? : Hello XBMC
        Enter your plugin id. [plugin.video.helloxbmc]: 
        Enter parent folder (where to create project) [/tmp]: 
        Enter provider name : Jonathan Beluch (jbel)
        Projects successfully created in /tmp/plugin.video.helloxbmc.
        Done.


Hello XBMC
----------

If you navigate to the newly created folder ``plugin.video.helloxbmc``, you'll
find an ``addon.py`` exactly like the one below.

.. sourcecode:: python

    #!/usr/bin/env python
    from xbmcswift import Plugin

    PLUGIN_NAME = 'Hello XBMC'
    PLUGIN_ID = 'plugin.video.helloxbmc'

    plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

    @plugin.route('/')
    def index():
        item = {'label': 'Hello XBMC!'}
        return plugin.finish([item])

    if __name__ == '__main__':
        plugin.run()

The above code is a fully functioning XBMC addon (not that it does much!). So
what does the code do?

1. After importing the Plugin class, we create our plugin instance. The
   arguments are, ``Addon Name``, ``addon id`` (ids should be according to
   XBMC's documentation <http://here>). The third argument is the actual file,
   which xbmcswift uses for some functionality behind the scenes.

2. We are using the ``plugin.route`` decorator on the ``index`` function. We
   are binding a url path of '/' to the index function. ('/' is the default URL
   path).

3. The index function creates a dictionary with a single key/val pair,
   ``label``. :meth:`~shityeah </xbmcswift.Plugin.finish>` expects a list, so we wrap our item in square
   brackets. Note the use of the return statement. In order for xbmcswift to
   function properly, each view must return ListItems (more on this later).

4. We simply call ``plugin.run()``.


Running Addons from the Command Line
------------------------------------

One of the shining points of XBMC is the ability to run plugins from the
command line. To do so, simply run addon.py like you would any other python
file::

    $ python addon.py
    --
    [0] Hello XBMC! (None)

The line with ``[0]`` corresponds to our added list item. Since our addon is
pretty simple, there is only one listitem available. A more complicated addon
might have output like this::

    $ python addon.py
    --
    [1] Subjects (special://plugin.video.academicearth/subjects/)
    [2] Universities (special://plugin.video.academicearth/universities/)
    [3] Instructors (special://plugin.video.academicearth/instructors/)

Here we can see the item number in square brackets, the label next, and the
path for the list item in parentheses.

There are 3 run modes available when running from the CLI, ``once``,
``interactive`` and ``crawl``. You can run ``python addon.py -h`` if you need
to refresh.

``once`` is the default mode, the one we ran above. If we run with
``interactive``, we'll be able to step through our addon by selecting items
from the list::

    $ python addon.py interactive
    --
    [0] Hello XBMC! (None)
    Choose an item or "q" to quit:

Note, that since we don't have an associated path for the list item, we'll get
an error if we choose 0.

See <http://this.link.> to read more about options when running from the command line.


Url Routing
-----------

One of the advantages of using xbmcswift, is its clean URL routing code. This
means you don't have to write your own code to parse the URL provided by XBMC
and route it to a specific piece of code. xbmcswift uses a a path passed to the
:meth:`~xbmcswift.Plugin.route` decorator to bind a URL to a function. For
example, a route of ``/videos/`` will result in a URL of
``plugin://plugin.video.helloxbmc/videos/`` to call the decorated function.

It's even possible to pass variables to functions, from the URLs. You might
have a function like this to list videos for a given category:

.. sourcecode:: python

    @plugin.route('/categories/<category>/')
    def show_videos(category):
        # Get videos for the provided category
        items = get_video_items(category)
        return plugin.finish(items)

Currently, there is no type coersion, so all variables plucked from URLs will
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
        return plugin.finish(items)


    @plugin.route('/labels/<label>/')
    def show_label(label):
        # Normally we would use label to parse a specific web page, in this case we are just
        # using it for a new list item label to show how URL parsing works.
        items = [
            {'label': label},
        ]
        return plugin.finish(items)

Let's run our plugin interactively now to explore::

    $ python addon.py interactive
    --
    [0] Hola XBMC! (plugin://plugin.video.helloxbmc/labels/spanish/)
    [1] Bonjour XBMC! (plugin://plugin.video.helloxbmc/labels/french/)
    Choose an item or "q" to quit: 0
    --
    [0] spanish (None)

Going back to our modified code, we are calling ``plugin.url_for`` to get the
URL for a specific view. The first and only required argument is the name of
our target function. If the function takes arguments, then we must pass keyword
arguments with the same variable names, hence ``label='spanish'``.

To learn more about URL routing and other available options, check out the <API>
or the <patterns page>.


Playing Media
-------------

The last thing we haven't covered is how to play an actual video. By default,
all items passed to plugin.finish are directory list items. This means that
their associated paths will call back into the addon. To differentiate playable
items, we'll set ``is_playable`` to ``True`` in our item dictionary.

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

As you can see, the URL is a direct link to a video asset, we are not calling
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
advanced functionality that xbmcswift doesn't support. However, if you still
want to be able run plugins from the command line you should import the xbmc
modules from xbmcswift, e.g.

.. sourcecode:: python

   from xbmcswift import xbmc, xbmcgui

Since these modules are written in C, they are only available when running
XBMC. To make plugins run on the command line, XBMC has mock versions of these
modules.


Going further
-------------
 
This should be enough to get started with your first simple XBMC addon. If
you'd like more information, please check out the detailed :ref:`tutorial` and
also review common :ref:`patterns`.
