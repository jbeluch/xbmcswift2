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

If you are scraping a website that uses pagination, it's possible to present
the same interface in XBMC without having to scrape all of the pages up front.
To accomplish this, we are going to create our own *Next* and *Previous* list
items which go the next and previous page of results respectively. We're also
going to take advantage of a parameter option that gets passed to XBMC,
`updateListing`. If we pass True for this parameter, then every time the use
clicks the Next item, the URL won't be added to history. This enables the ".."
list item to go to the correct parent directory, instead of the previous page.

Some example code:

.. sourcecode:: python

    @plugin.route('/videos/<page>')
    def show_videos(page='1'):
        page = int(page)  # all url params are strings by default
        videos, next_page = get_videos(page)
        items = [make_item(video) for video in videos]

        if next_page:
            items.insert(0, {
                'label': 'Next >>',
                'path': plugin.url_for('show_videos', page=str(page + 1))
            })
            
        if page > 1:
            items.insert(0, {
                'label': '<< Previous',
                'path': plugin.url_for('show_videos', page=str(page - 1))
            })

        return plugin.finish(items, update_listing=True)

The first thing to notice about our view, is that it takes a page number as a 
URL parameter. We then pass the page number to the API call, get_videos(), to
return the correct data based on the current page. Then we create our own
previous/next list items depending on the current page. Lastly, we are
returning the result of the call to plugin.finish(). By default, when you
normally return a list of dicts, plugin.finish() is called for you. However, in
this case we need to pass the update_listing=True parameter so we must call it
explictly.

Setting update_listing to True, notifies XBMC that we are paginating, and that
every new page should *not* be a new entry in the history.


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
    @plugin.route('/silents/', name='show_silent_genres', options={'path': 'index.php/silent-films-menu'})
    @plugin.route('/serials/', name='show_serials', options={'path': 'index.php/serials'})
    def show_genres(path='movies'):
        pass


Adding sort methods
-------------------

Sort methods enable the user to sort a directory listing in different ways. You
can see the available sort methods `here
<http://mirrors.xbmc.org/docs/python-docs/xbmcplugin.html#-addSortMethod>`_, or
by doing ``dir(xbmcswift2.SortMethod)``. The simplest way to add sort methods to
your views is to call plugin.finish() with a sort_methods argument and return
the result from your view (this is what xbmcswift2 does behind the scenes
normally).

.. sourcecode:: python

    @plugin.route('/movies')
    def show_movies():
        movies = api.get_movies()
        items = [create_item(movie) for movie in movies]
        return plugin.finish(items, sort_methods=['playlist_order', 'title', 'date'])

See :meth:`xbmcswift2.Plugin.finish` for more information.


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


Using the Context Menu
----------------------

XBMC allows plugin to authors to update the context menu on a per list item
basis. This allows you to add more functionality to your addons, as you can
allow users other actions for a given item. One popular use for this feature is
to create allow playable items to be added to custom playlists within the
addon. (See the itunes_ or reddit-music_ addons for implementations).

.. _itunes: https://github.com/dersphere/plugin.video.itunes_podcasts
.. _reddit-music: https://github.com/jbeluch/xbmc-reddit-music

In xbmcswift2, adding context menu items is accomplished by passing a value for
the *context_menu* key in an item dict. The value should be a list of 2-tuples.
Each tuple corresponds to a context menu item, and should be of the format
(display_string, action) where action is a string corresponding to one of
XBMC's `built-in functions`_. See `XBMC's documentation
<http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-addContextMenuItems>`_
for more information.

.. _`built-in functions`: http://wiki.xbmc.org/?title=List_of_Built_In_Functions

The most common actions are `XBMC.RunPlugin()` and `XBMC.Container.Update()`.
RunPlugin takes a single argument, a URL for a plugin (you can create a URL
with :meth:`xbmcswift2.Plugin.url_for`). XBMC will then run your plugin in a
background thread, *it will not affect the current UI*. So, RunPlugin is good
for any sort of background task. Update(), however will change the current UI
directory, so is useful when data is updated and you need to refresh the
screen.

If you are using one of the two above built-ins, there are convenience
functions in xbmcswift2 in the actions module.

Here is a quick example of updating the context menu.

.. sourcecode:: python

    from xbmcswift2 import actions

    @plugin.url('/favorites/add/<url>')
    def add_to_favs(url):
        # this is a background view
        ...

    def make_favorite_ctx(url)
        label = 'Add to favorites'
        new_url = plugin.url_for('add_to_favorites', url=url)
        return (label, actions.background(new_url))


    @plugin.route('/movies')
    def show_movies()
        items = [{
            ...
            'context_menu': [
                make_favorite_ctx(movie['url']),
            ],
            'replace_context_menu': True,
        } for movie in movies]
        return items

Sometimes the context_menu value can become very nested, so we've pulled out
the logic into the ``make_favorite_ctx`` function. Notice also the use of the
*replace_context_menu* key and the True value. This instructs XBMC to clear the
context menu prior to adding your context menu items. By default, your context
menu items are mixed in with the built in options.


Using extra parameters in the query string
------------------------------------------

When calling :meth:`xbmcswift.Plugin.url_for`, any keyword arguments passed
that are not required for the specified view function will be added as query
string arguments.

A dict of query string parameters can be accessed from ``plugin.request.args``.

Any arguments that are not instances of basestring will attempt to be preserved
by pickling them before being encoded into the query string. This functionality
isn't fully tested however, and XBMC does limit the length of URLs. If you need
to preserve python objects between function calls, see the Caching_ patterns.


Using Modules
-------------

Modules are meant to be mini-addons. They have some basic functionality that
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



