import os
import sys
import pickle
import xbmcswift2
from urllib import urlencode
from functools import wraps
from optparse import OptionParser
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from listitem import ListItem
from log import log
from common import enum
from common import clean_dict
from urls import UrlRule, NotFoundException, AmbiguousUrlException
from xbmcswift2 import (xbmc, xbmcgui, xbmcplugin, xbmcaddon, Request,)
from xbmcswift2.log import setup_log

from xbmcmixin import XBMCMixin
from common import Modes, DEBUG_MODES


class Plugin(XBMCMixin):
    '''Encapsulates all the properties and methods necessary for running an
    XBMC plugin.'''

    def __init__(self, name, addon_id, filepath):
        '''Initialize a plugin object for an XBMC addon. The required
        parameters are plugin name, addon_id, and filepath of the
        python file (typically in the root directory).
        '''
        self._name = name
        self._filepath = filepath
        self._addon_id = addon_id
        self._routes = []
        self._view_functions = {}
        self._addon = xbmcaddon.Addon(id=self._addon_id)
        self._current_items = []  # Keep track of added list items
        self._request = None  # Initialized when plugin.run() is called
        self._end_of_directory = False

        # set up logger
        self._log = setup_log(addon_id)

        # There will always be one request in each python thread...however it
        # should be moved out of plugin...
        self._cache_path = xbmc.translatePath(
            'special://profile/addon_data/%s/.cache/' % self._addon_id)

        # If we are runing in CLI, we need to load the strings.xml manually
        # TODO: a better way to do this. Perhaps allow a user provided filepath
        if xbmcswift2.CLI_MODE:
            from xbmcswift2.mockxbmc import utils
            utils.load_addon_strings(self._addon,
                os.path.join(os.path.dirname(self._filepath), 'resources',
                             'language', 'English', 'strings.xml'))

    @property
    def log(self):
        return self._log

    @property
    def id(self):
        return self._addon_id

    @property
    def cache_path(self):
        return self._cache_path

    @property
    def addon(self):
        return self._addon

    @property
    def added_items(self):
        return self._current_items

    def clear_added_items(self):
        self._current_items = []

    @property
    def handle(self):
        return self.request.handle

    @property
    def request(self):
        if self._request is None:
            raise Exception('There is no request attached to this plugin yet.'
                            ' It appears `plugin.run()` has not been called.')
        return self._request

    @property
    def name(self):
        return self._name

    def _parse_request(self, url=None, handle=None):
        '''Handles setup of the plugin state, including request
        arguments, handle, mode.

        This method never needs to be called directly. For testing, see
        plugin.test()
        '''
        # To accomdate self.redirect, we need to be able to parse a full url as
        # well
        if url is None:
            url = sys.argv[0]
            if len(sys.argv) == 3:
                url += sys.argv[2]
        if handle is None:
            handle = sys.argv[1]
        return Request(url, handle)

    def register_module(self, module, url_prefix):
        '''Registers a module with a plugin. Requires a url_prefix that
        will then enable calls to url_for.'''
        module._plugin = self
        module._url_prefix = url_prefix
        for func in module._register_funcs:
            func(self, url_prefix)

    def cached_route(self, url_rule, name=None, options=None):
        '''A decorator to add a route to a view and also apply caching.
        '''
        route_decorator = self.route(url_rule, name=name, options=options)
        cache_decorator = self.cache()
        def new_decorator(func):
            return route_decorator(cache_decorator(func))
        return new_decorator

    def route(self, url_rule, name=None, options=None):
        '''A decorator to add a route to a view. name is used to
        differentiate when there are multiple routes for a given view.'''
        # TODO: change options kwarg to defaults
        def decorator(f):
            view_name = name or f.__name__
            self.add_url_rule(url_rule, f, name=view_name, options=options)
            return f
        return decorator

    def add_url_rule(self, url_rule, view_func, name, options=None):
        '''This method adds a URL rule for routing purposes. The
        provided name can be different from the view function name if
        desired. The provided name is what is used in url_for to build
        a URL.

        The route decorator provides the same functionality.
        '''
        rule = UrlRule(url_rule, view_func, name, options)
        if name in self._view_functions.keys():
            # TODO: Raise exception for ambiguous views during registration
            log.warning('Cannot add url rule "%s" with name "%s". There is already a view with that name' % (url_rule, name))
            self._view_functions[name] = None
        else:
            log.debug('Adding url rule "%s" named "%s" pointing to function "%s"' % (url_rule, name, view_func.__name__))
            self._view_functions[name] = rule
        self._routes.append(rule)

    def url_for(self, endpoint, **items):
        '''Returns a valid XBMC plugin URL for the given endpoint name.
        endpoint can be the literal name of a function, or it can
        correspond to the name keyword arguments passed to the route
        decorator.

        Raises AmbiguousUrlException if there is more than one possible
        view for the given endpoint name.
        '''
        if endpoint not in self._view_functions.keys():
            raise NotFoundException, ('%s doesn\'t match any known patterns.' %
                                      endpoint)

        rule = self._view_functions[endpoint]
        if not rule:
            # TODO: Make this a regular exception
            raise AmbiguousUrlException

        pathqs = rule.make_path_qs(items)
        return 'plugin://%s%s' % (self._addon_id, pathqs)

    def _dispatch(self, path):
        for rule in self._routes:
            try:
                view_func, items = rule.match(path)
            except NotFoundException:
                continue
            #return view_func(**items)
            #TODO: allow returns just dictionaries that will be passed to
            #      plugin.finish()
            log.info('Request for "%s" matches rule for function "%s"' % (path, view_func.__name__))
            listitems = view_func(**items)

            # Allow the returning of bare dictionaries so we can cache view
            if not self._end_of_directory:
                listitems = self.finish(listitems)
            return listitems
        raise NotFoundException, 'No matching view found for %s' % path

    def redirect(self, url):
        '''Used when you need to redirect to another view, and you only
        have the final plugin:// url.'''
        # TODO: Should we be overriding self.request with the new request?
        new_request = self._parse_request(url=url, handle=self.request.handle)
        log.debug('Redirecting %s to %s' % (self.request.path, new_request.path))
        return self._dispatch(new_request.path)

    def run(self):
        '''The main entry point for a plugin.'''
        if xbmcswift2.CLI_MODE:
            from xbmcswift2.cli import app
            app.plugin_runner(self)
        else:
            self._request = self._parse_request()
            log.debug('Handling incoming request for %s' % (self.request.path))
            return self._dispatch(self.request.path)
