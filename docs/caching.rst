.. _caching:


Caching and Storage
===================

xbmcswift2 offers a few options for caching and storage to help improve the
user experience of your addon. swift offers a simple storage mechanism that
allows you to store arbitraty python objects to use between requests.

Storing Arbitraty Python Objects
--------------------------------

All caches/storage objects in xbmcswift2 act like python dictionaries. So to
get a cache, simply call the ``get_storage`` method.

.. sourcecode:: python

    people = plugin.get_storage('people')

    # now we can use people like a regular dict
    people['jon'] = 'developer'
    people.update({'dave': 'accountant'})

    people.items()
    # [('jon', 'deveoper'), ('dave', 'accountant')]

Caches are automatically persisted to disk each time an addon finishes
execution. If you would like to sync the cache to disk manually, you can call
``cache.sync()`` directly. However, this is not normally necessary.


File Formats
------------

By default, caches are saved to disk in the pickle format. This is convenient
since it can store Python objects. However, you can also pass 'csv' or 'json'
for the ``file_format`` keyword arg to the get_storage call.


Expirations
------------

Caches also offer an optional argument, ``TTL``, which is the max lifetime for
objects specified in minutes.

.. sourcecode:: python

    people = plugin.get_storage('people', TTL=24)

Caching Decorator
-----------------

xbmcswift2 provides a convenient caching decorator to automatically cache the
output of a function. For example, suppose we have a function ``get_api_data``,
that goes out to a remote API and fetches lots of data. If the website only
updates the API once a day, it doesn't make sense to make this request every
time the addon is run. So we can use the caching decorator with a TTL argument.

.. sourcecode:: python

    @plugin.cached(TTL=60*24)
    def get_api_data();
        # make remote request
        data = get_remote_data()
        return data

The default TTL is 1 day if not provided.


Caching Views
-------------

It's also possible to cache views (functions decorated with
``plugin.route()``). To simplify addon code, there is a special decorator
called ``cached_route``. All of the arguments to cached_route are the same as
the regular ``route`` decorator. Currently, it is not possible to specify a TTL
for this decorator; it defaults to 24 hours.

.. sourcecode:: python

    @plugin.cached_route('/')
    def main_menu();
        # do stuff

.. warning:: This is only currently possible for views that return lists of
             dictionaries. If you call plugin.finish() you *cannot* currently
             cache the view. See the below section 'Caveats' for more
             information.

Caveats
-------

The caching features of xbmcswift2 are still young and thus have some potential
problems to be aware of.

* First, if you are calling ``plugin.finish`` from a view, it is not currently
  possible to cache the view. This is because there are a few side effects
  which happen in ``finish`` which would not be cached. If this is the case,
  perhaps you can move some functionality in your view into a new function, and
  cache that result instead.

* Ensure variables are part of your method signature. If you cache a given
  function, ensure that all possible inputs are in your method signature.
  xbmcswift2 uses the arguments passed to your function as the unique key for
  the cache. Therefore it's possible to cache different return values for
  different inputs for a function. But if you check some global state from
  inside your function, the caching logic will have no knowlege of this and
  will return the *wrong* result.

* Currently, caches can grow very large since they do not automatically purge
  themselves based on filesize. Depending on what you are caching, you might
  need to introduce some logic to clear the cache.

.. sourcecode:: python

    cache = plugin.get_cache('people')
    cache.clear()
    cache.sync()

* It's advisable to include caching as the final step in your development
  process. If you are still developing your addon, occasionally incorrect
  return values can be cached which will cause you headaches.
