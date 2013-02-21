.. _item:


The ListItem
============

xbmcswift2 prefers to represent XBMC list items as plain python dictionaries as
much as possible. Views return lists of dictionaries, where each dict
represents an XBMC listitem. The list of valid keys in an item dict can always
be validated by reviewing the available arguments to
:meth:`xbmcswift2.ListItem.from_dict`. However, we'll go into more detail here.

Valid keys in an item dict are:

* `label`_
* `label2`_
* `icon`_
* `thumbnail`_
* `path`_
* `selected`_
* `info`_
* `properties`_
* `context_menu`_
* `replace_context_menu`_
* `is_playable`_
* `info_type`_
* `stream_info`_

label
-----

A required string. Used as the main display label for the list item.


label2
------

A string. Used as the alternate display label for the list item.


icon
----

A path to an icon image.


thumbnail
---------

A path to a thumbnail image.


path
----

A required string.

For non-playable items, this is typically a URL for a different path in the
same addon. To derive URLs for other views within your addon, use
:meth:`xbmcswift2.Plugin.url_for`.

For playable items, this is typically a URL to a remote media file. (One
exception, is if you are using the set_resolved_url pattern, the URL will be
playable but will also call back into your addon.)


selected
--------

A boolean which will set the item as selected. False is default.


info
----

A dictionary of key/values of metadata information about the item. See the
`XBMC docs
<http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-setInfo>`_ for
a list of valid info items. Keys are always strings but values should be the
correct type required by XBMC.

Also, see the related `info_type`_ key.


properties
----------

A dict of properties, similar to info-labels. See
http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-setProperty for
more information.


context_menu
------------

A list of tuples, where each tuple is of length 2. The tuple should be (label,
action) where action is a string representing a built-in XBMC function. See the
`XBMC documentation
<http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-addContextMenuItems>`_
for more details and `Using the Context Menu` for some example code.


replace_context_menu
--------------------

Used in conjunction with `context_menu`. A boolean indicating whether to
replace the existing context menu with the passed context menu items. Defaults
to False.


is_playable
-----------

A boolean indicating whether the item dict is a playable item. False indicates
that the item is a directory item. Use True when the path is a direct media
URL, or a URL that calls back to your addon where set_resolved_url will be
used.


info_type
---------

Used in conjunction with `info`. The default value is usually configured
automatically from your addon.xml. See
http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-setInfo for
valid values.


stream_info
-----------

A dict where each key is a stream type and each value is another dict of stream
values. See
http://mirrors.xbmc.org/docs/python-docs/xbmcgui.html#ListItem-addStreamInfo
for more information.
