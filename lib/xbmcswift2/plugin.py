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
from console import parse_commandline, display_video
from urls import UrlRule, NotFoundException, AmbiguousUrlException
from xbmcswift2 import (xbmc, xbmcgui, xbmcplugin, xbmcaddon, Request,
    display_listitems, get_user_choice, display_video, continue_or_quit)
from xbmcmixin import XBMCMixin


#Modes = enum('XBMC', 'ONCE', 'CRAWL', 'INTERACTIVE')
#DEBUG_MODES = [Modes.ONCE, Modes.CRAWL, Modes.INTERACTIVE]
from common import Modes, DEBUG_MODES


class Plugin(XBMCMixin):
    '''Encapsulates all the properties and methods necessary for running an
    XBMC plugin.'''

    def __init__(self, name, addon_id, filepath, strings_fn=None,
                 testing=False):
        '''Initialize a plugin object for an XBMC addon. The required
        parameters are plugin name, addon_id, and filepath of the
        python file (typically in the root directory.

        strings_fn can be a full filepath to a strings.xml used only
        when testing plugins in the command line.

        if testing=True, then the caller will be responsible for
        passing a valid mode and arguments list to plugin.test().
        '''
        self._name = name
        self._filepath = filepath
        self._addon_id = addon_id
        self._strings_fn = strings_fn
        self._routes = []
        self._view_functions = {}
        self._addon = xbmcaddon.Addon(id=self._addon_id)
        self._current_items = []  # Keep track of added list items

        # If testing mode is enabled, it is the responsibility of the developer
        # to call plugin.test() to set up the proper state. A mode and an
        # arguments list can be passed directly.
        if not testing:
            self._parse_args()

        # There will always be one request in each python thread...however it
        # should be moved out of plugin...
        self._cache_path = xbmc.translatePath(
            'special://profile/addon_data/%s/.cache/' % self._addon_id)

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

    @property
    def handle(self):
        return self.request.handle

    @property
    def request(self):
        return self._request

    @property
    def name(self):
        return self._name

    def _parse_args(self, mode=None, args=None):
        '''Handles setup of the plugin state, including request
        arguments, handle, mode.

        This method never needs to be called directly. For testing, see
        plugin.test()
        '''
        if mode is not None and args is not None:
            # being called from a test
            self._mode = mode
            _, args = parse_commandline(args, self.id)
            # let args fall through already assigned in the method call
        elif xbmcswift2.CLI_MODE:
            ## In CLI mode, ignore first arg as it is the program name
            self._mode, args = parse_commandline(sys.argv[1:], self.id)
        else:
            # in xbmc mode, we are missing the first arg as program name
            self._mode = Modes.XBMC
            args = sys.argv
        self._request = Request(*args)

        # If we are on the command line, attempt to load the strings.xml so
        # calls to plugin.get_string still work correctly.
        if self._mode in DEBUG_MODES:
            from xbmcswift2.mockxbmc import utils
            if self._strings_fn is None:
                self._strings_fn = os.path.join(
                    os.path.dirname(self._filepath), 'resources', 'language',
                    'English', 'strings.xml')
            utils.load_addon_strings(self._addon, self._strings_fn)

    def _fake_run(self, url):
        '''Manually sets some vars on the current instance. Used instead of
        calling __init__ on an instance.'''
        # Need to re-initialize some things each time through since we aren't
        # creating a new plugin instance

        self._current_items = []  # Clear the list of currently added items
        query_string = ''
        if '?' in url:
            url, query_string = url.split('?', 1)
        #args = [url, self.request.handle, query_string]
        args = [url]
        if self._mode == Modes.XBMC:
            # Need to fake differently for XBMC, used for redirect command
            # TODO: fix this
            args.extend([self.request.handle, query_string])
            sys.argv = args
            self._parse_args()
            return self.run()
        return self.test(Modes.ONCE, args)

    def _interactive(self, path):
        '''Provides an interactive menu from the command line that emulates the
        simple list-like interface within XBMC.'''
        # First run the initial path
        items = [item for item in self._dispatch(path)
                 if not item.get_played()]

        selected_item = get_user_choice(items)
        while selected_item is not None:
            items = [item for item in self._fake_run(selected_item.get_path())]
            selected_item = get_user_choice(items)

    def _crawl(self, path):
        '''Performs a breadth-first crawl of all possible routes from the
        starting path. Will only visit a URL once, even if it is referenced
        multiple times in a plugin. Requires user interaction in between each
        fetch.
        '''
        visited = []
        to_visit = self._dispatch(path)
        item = to_visit.pop(0)

        while to_visit and continue_or_quit(item):
            visited.append(item)

            # Run the new listitem
            items = self._fake_run(item.get_path())

            # Filter new items by checking against urls_visited and
            # urls_tovisit
            unvisited = [item for item in items
                         if item not in visited and item not in to_visit]
            to_visit.extend(unvisited)
            item = to_visit.pop(0)

    def test(self, mode, args):
        '''The main entry point for a plugin.'''
        self._parse_args(mode, args)
        return self.run()

    def run(self):
        '''The main entry point for a plugin.'''
        dispatcher = {
            Modes.XBMC: self._dispatch,
            Modes.ONCE: self._dispatch,
            Modes.CRAWL: self._crawl,
            Modes.INTERACTIVE: self._interactive,
        }
        request_handler = dispatcher[self._mode]
        log.debug('Dispatching %s to %s' %(self.request.path, request_handler.__name__))
        return request_handler(self.request.path)

    def register_module(self, module, url_prefix):
        '''Registers a module with a plugin. Requires a url_prefix that
        will then enable calls to url_for.'''
        module._plugin = self
        module._url_prefix = url_prefix
        for func in module._register_funcs:
            func(self, url_prefix)

    def route(self, url_rule, name=None, options=None):
        '''A decorator to add a route to a view. name is used to
        differentiate when there are multiple routes for a given view.'''
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
            if self._mode in DEBUG_MODES:
                display_listitems([item for item in listitems if
                    isinstance(item, ListItem) and not item.get_played()])
            return listitems
        raise NotFoundException

    def redirect(self, url):
        '''Used when you need to redirect to another view, and you only
        have the final plugin:// url.'''
        return self._fake_run(url)
