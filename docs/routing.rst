.. _routing:


URL Routing
===========

If you just need a basic introduction to URL routing, you can check out
:ref:`quickstart` or :ref:`tutorial`. This page explains all of the options and
more advanced usage of URL routing.

Encoding Parameters in URLs
---------------------------

You can pass parameters between view functions but putting instances of
``<var_name>`` in your url patterns that are passed to the route decorator.

For instance, if I had a view that should take a category_id, my call to route
would look like so:

.. sourcecode:: python

    @plugin.route('/categories/<category_id>')
    def show_category(category_id):
        pass

xbmcswift2 will attempt to match any incoming URLs against that pattern, so all
of the following URLs would match:

    * ``/categories/123``
    * ``/categories/apples``
    * ``/categories/apples%3Dpears``

xbmcswift2 will then extract the part of the URL that machtes a pattern withing
the angle brackets and will call your view with those variables (variables will
always be strings). So if you have one pattern in your URL, your view function
should take at least one argument.

Multiple Parameters
-------------------

It's possible to pass more than one parameter.

.. sourcecode:: python

    @plugin.route('/categories/<category_id>/<subcategory>')
    def show_category(category_id, subcategory):
        pass

The order of the arguments will always match the order specified in the URL
pattern.


Multiple URL Patterns and Defaults
----------------------------------

Sometimes it becomes useful to resuse a view for a different URL pattern. It's
possible to bind more than one URL pattern to a view. Keep in mind however,
that to use ``url_for`` unambiguously, you'll need to provide the *name*
argument to ``route`` to differentiate the two.

.. sourcecode:: python

    @plugin.route('/categories/<category_id>', name='show_category_firstpage')
    @plugin.route('/categories/<category_id>/<page>')
    def show_category(category_id, page='0'):
        pass

So now two different URL patterns will match the show_category view. However,
since our first pattern doesn't include ``<page>`` in the pattern, we'll need
to provide a default to our function. We can either provide a default in the
method signature, like above, or we can pass a dict for the ``options`` keyword
argument to ``route``.:

.. sourcecode:: python

    @plugin.route('/categories/<category_id>', name='show_category_firstpage', options={'page': '0'})
    @plugin.route('/categories/<category_id>/<page>')
    def show_category(category_id, page):
        pass

In these two examples, we would build urls for the different routes like so:

.. sourcecode:: python

    # For the show_category_firstpage view
    plugin.url_for('show_category_firstpage', category_id='science')

    # For the show_category view
    plugin.url_for('show_category', category_id='science', page='3')


Extra Parameters
----------------

Ocassionaly you might need to pass an argument to a view, but you don't want to
necessarily want to clutter up the URL pattern. Any extra keyword arguments
passed to url_for, that don't match a variable name in the URL pattern, will be
appended as query string arguments. They can then be accessed using
``plugin.request.args``.

URL Encoding and Pickling
-------------------------

Currently all keyword arguments to ``url_for`` that match variable names in the
URL pattern must be instances of basestring. This means ints must be converted
first using ``str()``. Arguments will then be urlencoded/urlunencoded by
xbmcswift2.

Any extra arguments that will end up in the query string, will be pickled and
urlencoded automatically. This can be advantageous, if you want to store a
simple list or something. However, pickling and urlencoding a python object can
result in a very large URL and XBMC will only handle a finite length, so use
this feature judiciously.
