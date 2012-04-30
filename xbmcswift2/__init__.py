'''
    xbmcswift2
    ------------------

    A micro framework to enable rapid development of XBMC plugins.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
try:
    import xbmc
    import xbmcgui
    import xbmcplugin
    import xbmcaddon
    CLI_MODE = False
except ImportError:
    CLI_MODE = True

    from mock import MockClass

    # xbmc module
    from mockxbmc.xbmc import translatePath, log
    xbmc = MockClass()
    xbmc.translatePath = translatePath
    xbmc.log = log

    # xbmcgui module
    xbmcgui = MockClass()
    from mockxbmc.xbmcgui import ListItem as _ListItem
    xbmcgui.ListItem = _ListItem

    # xbmcplugin module
    xbmcplugin = MockClass()
    from mockxbmc import xbmcplugin as _xbmcplugin
    for attr_name, attr_value in  _xbmcplugin.__dict__.items():
        setattr(xbmcplugin, attr_name, attr_value)

    # xbmcaddon module
    xbmcaddon = MockClass()
    from mockxbmc.xbmcaddon import Addon
    xbmcaddon.Addon = Addon

    # xbmcvfs module
    xbmcvfs = MockClass()

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
