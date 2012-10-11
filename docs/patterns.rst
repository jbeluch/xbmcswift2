.. _patterns:


Patterns
========


Caching
-------

View Caching
````````````

Use the :meth:`~xbmcswift2.Plugin.cached_route` decorator instead of the normal
`route` decorator. This will cache the results of your view for 24 hours.

*NOTE:* You must be returning a list of plain dictionaries from your view and
cannot return plugin.finish(). This is due to a current limitation in the cache
which doesn't keep track of side effects such as a call to plugin.finish. If
you need to call plugin.finish() because you are passing non-default arguments,
then see the next example which uses plugin.cached().

.. sourcecode:: python

    @plugin.cached_route('/subjects/', options={'url': full_url('subjects')})
    def show_subjects(url):
        '''Lists available subjects found on the website'''
        html = htmlify(url)
        subjects = html.findAll('a', {'class': 'subj-links'})

        items = [{
            'label': subject.div.string.strip(),
            'path': plugin.url_for('show_topics', url=full_url(subject['href'])),
        } for subject in subjects]
        return items

General Function Caching
````````````````````````

To cache the results of any function call, simply use the
:meth:`~xbmcswift2.Plugin.cached` decorator. Keep in mind that the function name
along with the args and kwargs used to call the function are used as the cache
key. If your function depends on any variables in outer scope which could
affect the return value, you should pass in those variables explictly as args
to ensure a different cache entry is created.

.. sourcecode:: python

    @plugin.cached()
    def get_api_data():
        return download_data()

Storing Arbitrary Objects
`````````````````````````

You can always create your own persistent storage using
:meth:`~xbmcswift2.Plugin.get_storage`. The returned storage acts like a
dictionary, however it is automatically persisted to disk.

.. sourcecode:: python

    storage = plugin.get_storage('people')
    storage['jon'] = {'vehicle': 'bike'}
    storage['dave']      # Throws KeyError
    storage.get('dave')  # Returns None
    storage.clear()      # Clears all items from the storage

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
default keyword arguments to the ``route`` decorator. Also, the function itself
can use python's default argument syntax.

.. sourcecode:: python

    @plugin.route('/movies/', name='show_movie_genres')
    @plugin.route('/silents/', name='show_silent_genres', {'path': 'index.php/silent-films-menu'})
    @plugin.route('/serials/', name='show_serials', {'path': 'index.php/serials'})
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


Pickling parameters in URls
---------------------------


Using extra parameters in the query string
------------------------------------------

When calling :meth:`xbmcswift.Plugin.url_for`, any keyword arguments passed
that are not required for the specified view function will be added as query
string arguments.

A dict of query string parameters can be accessed from ``plugin.request.args``.

Any arguments that are not instances of basestring will attempt to be preserved
by pickling them before being encoded into the query string. This functionality
isn't fully tested however, and XBMC does finitely limit the length of URLs. If
you need to preserve python objects between function calls, see the Caching_
patterns.


Using Modules
-------------

Modules are meant to be mini-plugins. They have some basic functionality that
is separate from the main plugin. In order to be used, they must be registered
with a plugin.

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



