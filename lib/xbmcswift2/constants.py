'''
    xbmcswift2.constants
    --------------------

    This module contains the SortMethod class which mirrors XBMC
    constants.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
from xbmcswift2 import xbmcplugin


class SortMethod(object):
    '''Static class to hold all of the available sort methods. The
    methods are dynamically imported from xbmcplugin. The prefix of
    'SORT_METHOD_' is automatically stripped.

    e.g. SORT_METHOD_TITLE becomes SortMethod.TITLE
    '''
    pass


PREFIX = 'SORT_METHOD_'
for attr_name, attr_value in xbmcplugin.__dict__.items():
    if attr_name.startswith(PREFIX):
        setattr(SortMethod, attr_name[len(PREFIX):], attr_value)
