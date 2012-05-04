from unittest import TestCase
from xbmcswift2 import Plugin
import xbmcswift2
from contextlib import contextmanager
from mock import Mock, patch
import sys


@contextmanager
def preserve_cli_mode(cli_mode):
    existing = xbmcswift2.CLI_MODE
    xbmcswift2.CLI_MODE = cli_mode
    yield
    xbmcswift2.CLI_MODE = existing

class TestInXBMCMode(TestCase):

    def test_init(self):
        name = 'Hello XBMC'
        plugin_id = 'plugin.video.helloxbmc'
        path = __file__
        plugin = Plugin(name, plugin_id, path)

        self.assertEqual(plugin_id, plugin.id)
        self.assertEqual(plugin.name, name)
        # TODO: Figure out a good way to test these things
        #self.assertEqual(plugin.cache_path, 'asdf')
        #self.assertEqual(plugin.addon, 'asdf')
        self.assertEqual(plugin.added_items, [])
        self.assertRaises(Exception, getattr, plugin, 'handle')
        self.assertRaises(Exception, getattr, plugin, 'request')

class TestParseRequest(TestCase):

    def setUp(self):
        name = 'Hello XBMC'
        plugin_id = 'plugin.video.helloxbmc'
        path = __file__
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
    path = __file__
    return Plugin(name, plugin_id, path)

def _TestPluginRunner(plugin):
    def run(relative_url, handle=0, qs='?'):
        url = 'plugin://%s%s' % (plugin.id, relative_url)
        sys.argv = [url, handle, qs]
        items =  plugin.run()
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
            self.assertEqual('Hello jon', resp[0].get_label())
            print resp
            resp = test_run('/dave/')
            print resp
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
