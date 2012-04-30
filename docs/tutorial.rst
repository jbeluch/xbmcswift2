.. _tutorial:

Tutorial
========

Intial views
------------


Using the strings file
----------------------


Check dependencies in addon.xml
-------------------------------


Basic xbmcswift views
--------------------------

XBMC addons typically add items to the screen using xbmc.addDirectoryItem.
These are items are either folders (a non-playable item which calls back into
the addon) or they are playable items which have an associated path to a media
file.


Adding non-playable list items
``````````````````````````````

The easiest way to add items using xbmcswift is to call the
:meth:`~xbmcswift.Plugin.finish` method on your plugin instance.  This method
takes a list of items as its first argument. The list of items can either be
instances of :class:`xbmcswift.ListItem` or dictionaries. If they are
dictionaries, the keys correspond to the arguments to the static method
:meth:`~xbmcswift.ListItem.from_dict`.

.. sourcecode:: python

    @plugin.route('/')
    def index():
        items = [
            {'label': 'Item One'},
            {'label': 'Item Two'},
        ]
        return plugin.finish(items)

Note, that we are returning the result of plugin.finish(). This enables us to
use all the helpful features of xbmcswift, like testing from the CLI.  The
above code will render two list items in XBMC. (Note that this example is not
complete since the items don't have a path associated with them, you would get
an error in XBMC if you clicked on one of them.

Adding playable list items
``````````````````````````

To add playable list items, simply set ``is_playable`` to ``True`` in the item
dict.

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
    
The above code will add a single list item to XBMC, which when selected will
play the specified video.


Initial Menu
------------

Typically most plugins will have an initial menu of hard-coded choices, so
we'll go ahead and do that.

We'll use the default view created in the skeleton, the view with route '/':

.. sourcecode:: python

    return plugin.add_items('asdfasdf')

Links to Other Views
--------------------

more text
asdf

Running from the command-line
-----------------------------

howh ot run from CLI

Providing a specific url
````````````````````````
how to provide url

Run modes
`````````
different run modes, interactive, once, <test> link to testing patterns

Returning from Views
--------------------

Returns directoires
```````````````````

Returning ListItems
```````````````````

Returning using set_resolved_url
````````````````````````````````


Running from XBMC
-----------------
how to run new plugin in xbmc
use symlinks?
