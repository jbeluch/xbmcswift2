'''
    xbmcswift2.mock
    ---------------

    This module contains the MockClass object, used for mocking XBMC
    python modules when running in CLI mode.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
class MockClass(object):
    '''This is a base class used for stubbing out a class. It
    always returns a callable and will never raise an AttributeError.
    '''
    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            '''A silent callable method'''
            return self
        return mock_method
