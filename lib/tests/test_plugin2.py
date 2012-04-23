import os
from unittest import TestCase
import sys
from contextlib import contextmanager
from mock import Mock, patch
from xbmcswift2 import Plugin
from xbmcswift2 import xbmcaddon
from xbmcswift2 import Modes
import xbmcswift2

TEST_STRINGS_FN = os.path.join(os.path.dirname(__file__), 'data', 'strings.xml')

@contextmanager
def preserve_cli_mode():
    existing = xbmcswift2.CLI_MODE
    yield
    xbmcswift2.CLI_MODE = existing

@contextmanager
def cache_value(name):
    #if '.' in name:
        #base, _ = name.split('.', 1)
        #__import__(base)
    # recursively call getattr
    #value = getattr(obj, attr)

    # works for 1 period
    base, name = name.split('.')
    value = getattr(xbmcswift2, name)
    yield
    setattr(xbmcswift2, name, value)



class TestAsXBMC(TestCase):

    def test_init(self):
        sys.argv = ['plugin://plugin.video.helloxbmc/videos/', '0', '?']
        with preserve_cli_mode():
            xbmcswift2.CLI_MODE = False
            plugin = Plugin('Hello XBMC', 'plugin.video.helloxbmc', __file__)

        self.assertEqual('plugin.video.helloxbmc', plugin.id)
        self.assertEqual('Hello XBMC', plugin.name)
        assert isinstance(plugin.addon, xbmcaddon.Addon)
        self.assertEqual('/tmp/xbmcswift2_debug/profile/addon_data/plugin.video.helloxbmc/.cache', plugin.cache_path)
        self.assertEqual([], plugin.added_items)
        self.assertEqual(0, plugin.handle)
        self.assertEqual(Modes.XBMC, plugin._mode)
        # TODO: test request
        #self.assertEqual(plugin.request)

    def test_with_query_args(self):
        sys.argv = ['plugin://plugin.video.helloxbmc/videos/', '0', '?foo=bar']
        with preserve_cli_mode():
            xbmcswift2.CLI_MODE = False
            plugin = Plugin('Hello XBMC', 'plugin.video.helloxbmc', __file__)

        self.assertEqual({'foo': ['bar']}, plugin.request.args)

class TestRouting(TestCase):
    def setUp(self):
        sys.argv = ['.plugin.py']
        self.p = Plugin('Hello XBMC', 'plugin.video.helloxbmc', __file__, TEST_STRINGS_FN)

    def test_min_args(self):
        @self.p.route('/')
        def watch_videos(self):
            pass 
        






    # test default args
    # test multipe names for a view
    # test ambiguous no match incoming url
    # test ambiguous url registering












