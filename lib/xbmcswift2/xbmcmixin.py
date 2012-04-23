import os
import sys
import time
import shelve
from datetime import timedelta
from functools import wraps

import xbmcswift2
from xbmcswift2 import xbmc, xbmcaddon, xbmcplugin
from xbmcswift2.cache import Cache, TimedCache
from common import Modes, DEBUG_MODES
from console import parse_commandline
from request import Request
from console import parse_commandline, display_video


class XBMCMixin(object):
    '''A mixin to add XBMC helper methods. In order to use this mixin,
    the child class must implement the following methods and
    properties:

        def cache_path(self, path)

        self.cache_path
        self.addon
        self.added_items
        self.request
    _end_of_directory = False
    _memoized_cache = None
    _unsynced_caches = None
    '''

    def cache(self, ttl_hours=24):
        '''View caching decorator. Currently must be closest to the
        view because route decorators don't wrap properly.
        '''
        def decorating_function(function):
            cache = self.get_timed_cache('function_cache', file_format='pickle',
                                         ttl=timedelta(hours=ttl_hours))
            kwd_mark = 'f35c2d973e1bbbc61ca60fc6d7ae4eb3'

            @wraps(function)
            def wrapper(*args, **kwargs):
                key = (function.__name__, kwd_mark,) + args
                if kwargs:
                    key += (kwd_mark,) + tuple(sorted(kwargs.items()))

                try:
                    result = cache[key]
                    print 'Cache hit!'
                except KeyError:
                    print 'Cache miss :('
                    result = function(*args, **kwargs)
                    cache[key] = result
                cache.sync()
                return result
            return wrapper
        return decorating_function

    def _get_cache(self, cache_type, cache_name, **kwargs):
        if not hasattr(self, '_unsynced_caches'):
            self._unsynced_caches = {}
        filename = os.path.join(self.cache_path, cache_name)
        try:
            cache = self._unsynced_caches[filename]
        except KeyError:
            cache = cache_type(filename, **kwargs)
            self._unsynced_caches[filename] = cache
        return cache

    def get_timed_cache(self, cache_name, file_format='pickle', ttl=None):
        return self._get_cache(TimedCache, cache_name, file_format=file_format, ttl=ttl)

    def get_cache(self, cache_name, file_format='pickle'):
        return self._get_cache(TimedCache, cache_name, file_format=file_format)

    def cache_fn(self, path):
        # TODO:
        #if not os.path.exists(self._cache_path):
            #os.mkdir(self._cache_path)
        return os.path.join(self.cache_path, path)

    def temp_fn(self, path):
        return os.path.join(xbmc.translatePath('special://temp'), path)

    def get_string(self, stringid):
        '''Returns the localized string from strings.xml for the given
        stringid.
        '''
        return self.addon.getLocalizedString(stringid)

    def set_content(self, content):
        '''Sets the content type for the plugin.'''
        # TODO: Change to a warning instead of an assert. Otherwise will have
        # to keep this list in sync with
        #       any XBMC changes.
        #contents = ['files', 'songs', 'artists', 'albums', 'movies',
        #'tvshows', 'episodes', 'musicvideos']
        #assert content in contents, 'Content type "%s" is not valid' % content
        xbmcplugin.setContent(self.handle, content)

    def get_setting(self, key):
        #TODO: allow pickling of settings items?
        # TODO: STUB THIS OUT ON CLI
        return self.addon.getSetting(id=key)

    def set_setting(self, key, val):
        # TODO: STUB THIS OUT ON CLI
        return self.addon.setSetting(id=key, value=val)

    def open_settings(self):
        '''Opens the settings dialog within XBMC'''
        self.addon.openSettings()

    def add_to_playlist(self, items, playlist='video'):
        '''Adds the provided list of items to the specified playlist.
        Available playlists include *video* and *music*.
        '''
        playlists = {'music': 0, 'video': 1}
        assert playlist in playlists.keys(), ('Playlist "%s" is invalid.' %
                                              playlist)
        selected_playlist = xbmc.PlayList(playlists[playlist])

        _items = []
        for item in items:
            if not hasattr(item, 'as_xbmc_listitem'):
                item = xbmcswift2.ListItem.from_dict(**item)
            _items.append(item)
            selected_playlist.add(item.get_path(), item.as_xbmc_listitem())
        return _items

    def set_resolved_url(self, url):
        item = xbmcswift2.ListItem(path=url)
        item.set_played(True)
        xbmcplugin.setResolvedUrl(self.handle, True, item.as_xbmc_listitem())

        if self._mode in DEBUG_MODES:
            display_video(item)
        return [item]

    def play_video(self, item, player=xbmc.PLAYER_CORE_DVDPLAYER):
        if not isinstance(item, xbmcswift2.ListItem):
            item = xbmcswift2.ListItem.from_dict(**item)
        item.set_played(True)
        xbmc.Player(player).play(item.get_path, item)

        if self._mode in DEBUG_MODES:
            display_video(item)
        return [item]

    def add_items(self, items):
        '''Adds ListItems to the XBMC interface. Each item in the
        provided list should either be instances of xbmcswift2.ListItem,
        or regular dictionaries that will be passed to
        xbmcswift2.ListItem.from_dict. Returns the list of ListItems.
        '''
        # For each item if it is not already a list item, we need to create one
        _items = []

        # Create ListItems for anything that is not already an instance of
        # ListItem
        for item in items:
            if not isinstance(item, xbmcswift2.ListItem):
                item = xbmcswift2.ListItem.from_dict(**item)
            _items.append(item)

        tuples = [item.as_tuple() for item in _items]
        xbmcplugin.addDirectoryItems(self.handle, tuples, len(tuples))

        # We need to keep track internally of added items so we can return them
        # all at the end for testing purposes
        self.added_items.extend(_items)

        # Possibly need an if statement if only for debug mode
        return _items

    def end_of_directory(self, succeeded=True, update_listing=False,
                         cache_to_disc=True):
        '''Wrapper for xbmcplugin.endOfDirectory. Records state in
        self._end_of_directory.

        Typically it is not necessary to call this method directly, as
        calling plugin.finish will call this.
        '''
        if not self._end_of_directory:
            self._end_of_directory = True
            # Finalize the directory items
            return xbmcplugin.endOfDirectory(self.handle, succeeded,
                                             update_listing, cache_to_disc)
        assert False, 'Already called endOfDirectory.'

    def finish(self, items=None, sort_methods=None, succeeded=True,
               update_listing=False, cache_to_disc=True):
        '''Adds the provided items to the XBMC interface. Each item in
        the provided list should either be an instance of
        xbmcswift2.ListItem or a dictionary that will be passed to
        xbmcswift2.ListItem.from_dict().

        sort_methods should be a list of valid XBMC sort_methods. The
        reamaining keyword arguments are passed along to
        xbmcplugin.endOfDirectory.

        Returns a list of all ListItems added to the XBMC interface.
        '''
        # If we have any items, add them. Items are optional here.
        if items:
            self.add_items(items)
        if sort_methods:
            for sort_method in sort_methods:
                xbmcplugin.addSortMethod(self.handle, sort_method)

        # Finalize the directory items
        xbmcplugin.endOfDirectory(self.handle, succeeded,
                                  update_listing, cache_to_disc)

        # Close any open caches which will persist them to disk
        if hasattr(self, '_unsynced_caches'):
            for cache in self._unsynced_caches.values():
                cache.close()

        # Return the cached list of all the list items that were added
        return self.added_items


#class XBMCProxyMixin(XBMCMixin):

    #_PROXY_METHODS = [ 'add_items', 'end_of_directory', 'finish', 'cache_fn',
        #'temp_fn', 'get_string', 'set_content', 'get_setting', 'set_setting',
        #'open_settings', 'add_to_playlist', 'set_resolved_url', 'play_video',
    #]
    #def __get_item__(self, attr):
        #if attr in Module._PROXY_METHODS:
            #_validate_registered(self)
            #return getattr(self.plugin, attr)
        ##return normal
        #pass

    # TODO: write some code (metaclass?) that appends a registration
    # required message to every method's __doc__  in _PROXY_METHODS
