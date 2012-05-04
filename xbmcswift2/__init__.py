'''
    xbmcswift2
    ------------------

    A micro framework to enable rapid development of XBMC plugins.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
from types import ModuleType


class module(ModuleType):
    '''A wrapper class for a module used to override __getattr__. This class
    will behave normally for any existing module attributes. For any attributes
    which do not existin in the wrapped module, a mock function will be
    returned. This function will also return itself enabling multiple mock
    function calls.
    '''

    def __init__(self, wrapped=None):
        self.wrapped = wrapped

    def __getattr__(self, name):
        '''Returns any existing attr for the wrapped module or returns a mock
        function for anything else. Never raises an AttributeError.
        '''
        try:
            return getattr(self.wrapped, name)
        except AttributeError:
            def func(*args, **kwargs):
                '''A mock function which returns itself, enabling chainable
                function calls.
                '''
                log.warning('The %s method has not been implented on the CLI. '
                            'Your code might not work properly when calling '
                            'it.' % name)
                return self
            return func


try:
    import xbmc
    import xbmcgui
    import xbmcplugin
    import xbmcaddon
    CLI_MODE = False
except ImportError:
    CLI_MODE = True
    # TODO: delete unneeded modules

    import sys
    from log import log

    # Mock the XBMC modules
    from mockxbmc import xbmc, xbmcgui, xbmcplugin, xbmcaddon
    xbmc = module(xbmc)
    xbmcgui = module(xbmcgui)
    xbmcplugin = module(xbmcplugin)
    xbmcaddon = module(xbmcaddon)
    xbmcvfs = module()


# Now get on with the xbmcswift stuff
from request import Request
from common import (pickle_dict, unpickle_dict, clean_dict,
    download_page, unhex)
import constants
from plugin import Plugin, Modes
from xbmcmixin import XBMCMixin
from module import Module
from urls import (AmbiguousUrlException, NotFoundException, UrlRule)
from listitem import ListItem
