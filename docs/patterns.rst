.. _patterns:


Patterns
========


Adding pagination
-----------------

pagination


Reusing views with multiple routes
----------------------------------

It is possible to decorate views with more than one route. This becomes useful
if you are parsing different URLs that share the same parsing code. In order to
unambiguously use :meth:`~xbmcswift.Plugin.url_for`, you need to pass a value
for the name keyword argument. When calling ``url_for``, you pass this
specified name instead of the name of the actual function.

If the decorated method requires arguments, it is possible to pass these as
extra keyword arguments to the ``route`` decorator if they don't need to be
dynamically pulled from the URL. Also, the function itself can use python's
default argument syntax.

.. sourcecode:: python

    @plugin.route('/movies/', name='show_movie_genres')
    @plugin.route('/silents/', name='show_silent_genres', path='index.php/silent-films-menu')
    @plugin.route('/serials/', name='show_serials', path='index.php/serials')
    def show_genres(path='movies'):
        pass


Adding sort methods
-------------------

sort methods


Playing RTMP urls
-----------------

If we need to play an RTMP url, we can use :meth:`xbmcswift.Plugin.play_video`.

.. sourcecode:: python

    @plugin.route('/live/')
    def watch_live():
        item =  {
            'label': 'AlJazeera Live',
            'path': 'rtmp://aljazeeraflashlivefs.fplive.net:1935/aljazeeraflashlive-live/aljazeera_english_1 live=true',
        }
        return plugin.play_video(item)


Using settings
--------------

how to use settings


Using the context menu
----------------------


Using the plugin cache
----------------------

store arbiratry files in plugin cache


Pickling parameters in URls
---------------------------


Using extra parameters in the query string
------------------------------------------

When calling :meth:`xbmcswift.Plugin.url_for`, any keyword arguments passed
that are not required for the specified view function will be added as query
string arguments.

Query string parameters can be accessed from ``plugin.request.args``.

Any arguments that are not instances of basestring will attempt to be preserved
by pickling them before being encoded into the query string. This functionality
isn't fully tested however, and XBMC does finitely limit the length of URLs.


Using the plugin structure
--------------------------

Creating an add to favorites plugin:

.. sourcecode:: python

    from xbmcswift import Module

    playlist = Module(__name__)

    @playlist.route('/add/')
    def add_to_playlist():
        items = [playlist.qs_args]
            return playlist._plugin.add_to_playlist(items)

Examples of plugins
```````````````````

    * add to favorites
    * report to google form


Testing with Nose
-----------------

How to test with nose



