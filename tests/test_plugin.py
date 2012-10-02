import os
import sys
import shutil
from unittest import TestCase

from mock import Mock, patch

from xbmcswift2.mockxbmc.xbmc import TEMP_DIR
from xbmcswift2 import Plugin
import xbmcswift2

from utils import preserve_cli_mode, preserve_cwd

# Ensure we are starting clean by removing old test folders
try:
    shutil.rmtree(TEMP_DIR)
except OSError:
    # doesn't exist, just pass
    pass




class TestInit(TestCase):

    def test_init_cli_mode(self):
        name = 'Hello XBMC'
        plugin_id = 'plugin.video.helloxbmc'
        path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'addon.py')
        with preserve_cwd(os.path.dirname(path)):
            plugin = Plugin(name, plugin_id, path)

        self.assertEqual(plugin_id, plugin.id)
        self.assertEqual(plugin.name, name)
        self.assertEqual(plugin.info_type, 'video')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_init_cli_mode_default_args(self):
        name = 'Hello XBMC'
        with preserve_cwd(os.path.join(os.path.dirname(__file__), 'data', 'plugin')):
            plugin = Plugin()

        self.assertEqual('plugin.video.academicearth', plugin.id)
        self.assertEqual(plugin.name, 'Academic Earth')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_init_not_cli_mode(self):
        name = 'Hello XBMC'
        plugin_id = 'plugin.video.helloxbmc'
        path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'addon.py')
        with preserve_cwd(os.path.dirname(path)):
            with preserve_cli_mode(cli_mode=False):
                plugin = Plugin(name, plugin_id, path)

        self.assertEqual(plugin_id, plugin.id)
        self.assertEqual(plugin.name, name)
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_init_not_cli_mode_default_args(self):
        name = 'Hello XBMC'
        path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'addon.py')
        with preserve_cli_mode(cli_mode=False):
            with preserve_cwd(os.path.join(os.path.dirname(__file__), 'data', 'plugin')):
                plugin = Plugin()

        self.assertEqual('plugin.video.academicearth', plugin.id)
        self.assertEqual(plugin.name, 'Academic Earth')
        self.assertTrue(os.path.isdir(plugin.storage_path))
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

    def test_info_types(self):
        name = 'Hello XBMC'
        path = __file__

        # can't parse from id, default to video
        with preserve_cli_mode(cli_mode=False):
            with preserve_cwd(os.path.join(os.path.dirname(__file__), 'data', 'plugin')):
                plugin = Plugin(name, 'script.module.test', path)
                self.assertEqual(plugin.info_type, 'video')

                # parse from ID
                plugin = Plugin(name, 'plugin.audio.test')
                self.assertEqual(plugin.info_type, 'music')

                plugin = Plugin(name, 'plugin.video.test')
                self.assertEqual(plugin.info_type, 'video')

                plugin = Plugin(name, 'plugin.image.test')
                self.assertEqual(plugin.info_type, 'pictures')

                # info_type param should override value parsed from id
                plugin = Plugin(name, 'plugin.video.test', info_type='music')
                self.assertEqual(plugin.info_type, 'music')


class TestParseRequest(TestCase):

    def setUp(self):
        name = 'Hello XBMC'
        plugin_id = 'plugin.video.helloxbmc'
        path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'addon.py')
        with preserve_cwd(os.path.dirname(path)):
            self.plugin = Plugin(name, plugin_id, path)

    def test_parse_request(self):
        with patch('xbmcswift2.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.helloxbmc', '0', '?']
            self.plugin._parse_request()
            MockRequest.assert_called_with('plugin://plugin.video.helloxbmc?', '0')

    def test_parse_request_no_qs(self):
        with patch('xbmcswift2.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.helloxbmc', '0']
            self.plugin._parse_request()
            MockRequest.assert_called_with('plugin://plugin.video.helloxbmc', '0')

    def test_parse_request_path_in_arg0(self):
        # Older versions of xbmc sometimes pass path in arg0
        with patch('xbmcswift2.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.helloxbmc/videos/', '0', '?foo=bar']
            self.plugin._parse_request()
            MockRequest.assert_called_with('plugin://plugin.video.helloxbmc/videos/?foo=bar', '0')

    def test_parse_request_path_in_arg2(self):
        # Older versions of xbmc sometimes pass path in arg2
        with patch('xbmcswift2.plugin.Request') as MockRequest:
            sys.argv = ['plugin://plugin.video.helloxbmc', '0', '/videos/?foo=bar']
            self.plugin._parse_request()
            MockRequest.assert_called_with('plugin://plugin.video.helloxbmc/videos/?foo=bar', '0')


def NewPlugin():
    name = 'Hello XBMC'
    plugin_id = 'plugin.video.helloxbmc'
    path = os.path.join(os.path.dirname(__file__), 'data', 'plugin', 'addon.py')
    with preserve_cwd(os.path.dirname(path)):
        return Plugin(name, plugin_id, path)

def _TestPluginRunner(plugin):
    def run(relative_url, handle=0, qs='?'):
        url = 'plugin://%s%s' % (plugin.id, relative_url)
        sys.argv = [url, handle, qs]
        items =  plugin.run(test=True)
        plugin._end_of_directory = False
        plugin.clear_added_items()
        return items
    return run


class TestBasicRouting(TestCase):

    def test_url_for(self):
        plugin = NewPlugin()
        @plugin.route('/')
        def main_menu():
            return [{'label': 'Hello XBMC'}]
        self.assertEqual(plugin.url_for('main_menu'), 'plugin://plugin.video.helloxbmc/')
        self.assertEqual(plugin.url_for('main_menu', foo='bar'), 'plugin://plugin.video.helloxbmc/?foo=bar')
        self.assertEqual(plugin.url_for('main_menu', foo=3), 'plugin://plugin.video.helloxbmc/?foo=I3%0A.&_pickled=foo')

    def test_url_for_multiple_routes(self):
        plugin = NewPlugin()
        @plugin.route('/')
        @plugin.route('/videos/', name='videos')
        def main_menu():
            return [{'label': 'Hello XBMC'}]
        self.assertEqual(plugin.url_for('main_menu'), 'plugin://plugin.video.helloxbmc/')
        self.assertEqual(plugin.url_for('main_menu', foo='bar'), 'plugin://plugin.video.helloxbmc/?foo=bar')
        self.assertEqual(plugin.url_for('main_menu', foo=3), 'plugin://plugin.video.helloxbmc/?foo=I3%0A.&_pickled=foo')
        self.assertEqual(plugin.url_for('videos'), 'plugin://plugin.video.helloxbmc/videos/')

    def test_options(self):
        plugin = NewPlugin()
        @plugin.route('/person/<name>/', options={'name': 'dave'})
        def person(name):
            return [{'label': 'Hello %s' % name}]
        self.assertEqual(plugin.url_for('person', name='jon'), 'plugin://plugin.video.helloxbmc/person/jon/')
        self.assertEqual(plugin.url_for('person'), 'plugin://plugin.video.helloxbmc/person/dave/')

    def test_basic_routing(self):
        plugin = NewPlugin()
        @plugin.route('/')
        def main_menu():
            return [{'label': 'Hello XBMC'}]
        with preserve_cli_mode(cli_mode=False):
            test_run = _TestPluginRunner(plugin)
            resp = test_run('/')
            self.assertEqual('Hello XBMC', resp[0].get_label())

    def test_options_routing(self):
        plugin = NewPlugin()
        @plugin.route('/person/<name>/')
        @plugin.route('/')
        @plugin.route('/dave/', options={'name': 'dave'})
        def person(name='chris'):
            return [{'label': 'Hello %s' % name}]
        with preserve_cli_mode(cli_mode=False):
            test_run = _TestPluginRunner(plugin)
            resp = test_run('/person/jon/')
            print plugin.request.url
            self.assertEqual('Hello jon', resp[0].get_label())
            resp = test_run('/dave/')
            self.assertEqual('Hello dave', resp[0].get_label())
            resp = test_run('/')
            self.assertEqual('Hello chris', resp[0].get_label())

    #def test_route_conflict(self):
        # TODO this should raise an error
        #plugin = NewPlugin()
        #@plugin.route('/')
        #def jon():
            #return 'Hello jon'
        #@plugin.route('/')
        #def dave():
            #return 'Hello dave'
        #with preserve_cli_mode(cli_mode=False):
            #test_run = _TestPluginRunner(plugin)
            #resp = test_run('/')
            #self.assertEqual('Hello jon', resp)
            #self.assertEqual('Hello dave', resp)

    def test_redirect(self):
        plugin = NewPlugin()
        @plugin.route('/')
        def main_menu():
            url = plugin.url_for('videos')
            return plugin.redirect(url)
        @plugin.route('/videos/')
        def videos():
            return [{'label': 'Hello Videos'}]
        with preserve_cli_mode(cli_mode=False):
            test_run = _TestPluginRunner(plugin)
            resp = test_run('/')
            self.assertEqual('Hello Videos', resp[0].get_label())

class TestRegisterModule():
    pass
