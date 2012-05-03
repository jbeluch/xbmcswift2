.. _upgrading:

Upgrading from xbmcswift
========================

While the API for xbmcswift2 is very similar to xbmcswift, there are a few
backwards incompatible changes. The following list highlights the biggest
changes:

* Update all imports to use ``xbmcswift2`` instead of ``xbmcswift``. This
  includes the dependency in your addon.xml file.

* In list item dictionaries, the ``url`` keyword has been changed to ``path``.

* In xbmcswift views, the proper way to return from a view was
  ``return plugin.add_items(items)``. In xbmcswift2 you can either ``return
  plugin.finish(items)`` or more simply ``return items``.
    .. sourcecode:: python

        # xbmcswift
        return plugin.add_items(items)

        # xbmcswift2
        return plugin.finish(items)
        # (or)
        return items

* In the past, the ``plugin.route()`` decorator accepted arbitrary keyword
  arguments in the call to be used as defaults. These args must now be a single
  dictionary for the keyword arg ``options``.

.. sourcecode:: python

    # xbmcswift
    plugin.route('/', page='1')

    # xbmcswift2
    plugin.route('/', options={'page': '1'})

* In list item dictionaries, the ``is_folder`` keyword is no longer necessary.
  Directory list items are the default and require no special keyword. If you
  wish to create a playable list item, set the ``is_playable`` keyword to True.
