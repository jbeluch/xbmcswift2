#!/usr/bin/env python
from unittest import TestCase
import os
import xbmcswift2
from xbmcswift2 import Request
from xbmcswift2.console import parse_commandline
from xbmcswift2.plugin import Plugin
from xbmcswift2.module import Module
from xbmcswift2.urls import AmbiguousUrlException, UrlRule, NotFoundException
from xbmcswift2.mockxbmc import utils
from xbmcswift2 import ListItem
import sys
from mock import Mock, patch
from types import MethodType
from xbmcswift2.plugin import Modes


class TestPluginInit(TestCase):
    @patch('xbmcswift2.console.parse_commandline')
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    @patch('xbmcswift2.xbmcaddon.Addon')
    @patch('xbmcswift2.plugin.Request')
    @patch('xbmcswift2.xbmc.translatePath')
    def test_init_cli_mode(self, mock_translatePath, mock_Request, mock_Addon, mock_load_addon_strings, mock_parse_commandline):
        mock_parse_commandline.return_value = (Modes.ONCE, ['plugin://plugin.id/home/', '0', '?foo=bar'])
        mock_load_addon_strings.return_value = {}
        mock_Addon.return_value = 'Mock Addon'
        sys.argv = ['./addon.py', 'once', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')

        # necessary to call, only called when plugin.run or plugin.test is called
        #plugin._parse_args()

        self.assertEqual(plugin._name, 'Plugin Name')
        self.assertEqual(plugin._filepath, '.')
        self.assertEqual(plugin._addon_id, 'plugin.id')
        self.assertEqual(plugin._strings_fn, 'resources/language/English/strings.xml')
        self.assertEqual(plugin._routes, [])
        self.assertEqual(plugin._view_functions, {})
        mock_Addon.assert_called_with(id='plugin.id')
        self.assertEqual(plugin._mode, Modes.ONCE)
        mock_Request.assert_called_with('plugin://plugin.id/home/', '0', '?foo=bar')
        mock_load_addon_strings.assert_called_with('Mock Addon', 'resources/language/English/strings.xml')
        mock_translatePath.assert_called_with('special://profile/addon_data/plugin.id/.cache/')

    @patch('xbmcswift2.console.parse_commandline')
    @patch('xbmcswift2.xbmcaddon.Addon')
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_init_strings_fn(self, mock_load_addon_strings, mock_Addon, mock_parse_commandline):
        mock_parse_commandline.return_value = (Modes.ONCE, ['plugin://plugin.id/home/', '0', '?foo=bar'])
        mock_Addon.return_value = 'Mock Addon'
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.', strings_fn='strings.xml')
        mock_load_addon_strings.assert_called_with('Mock Addon', 'strings.xml')

    @patch('xbmcswift2.console.parse_commandline')
    @patch('xbmcswift2.plugin.Request')
    def test_init_xbmc_mode(self, mock_Request, mock_parse_commandline):
        xbmcswift2.CLI_MODE = False
        sys.argv = ['plugin://plugin.id/home/', '0', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        # necessary to call, only called when plugin.run or plugin.test is called
        plugin._parse_args()
        self.assertEqual(plugin._mode, Modes.XBMC)
        mock_Request.assert_called_with('plugin://plugin.id/home/', '0', '?foo=bar')
        xbmcswift2.CLI_MODE = True

class TestRegisterModule(TestCase):
    def test_register_module(self):
        module = Mock(spec=Module)
        plugin = Mock(spec=Plugin)

        # set the actual register_module method on our mocked plugin
        plugin.register_module = MethodType(Plugin.register_module, plugin)
            
        # set up the module's registered funcs
        f1, f2 = Mock(), Mock()
        module._register_funcs = [f1, f2]

        # Now register the module
        plugin.register_module(module, 'foobar')

        self.assertEqual(module._plugin, plugin)
        f1.assert_called_with(plugin, 'foobar')
        f2.assert_called_with(plugin, 'foobar')

class TestRouteDecorator(TestCase):
    def test_route_decorator_no_options(self):
        plugin = Mock(spec=Plugin)
        plugin.route = MethodType(Plugin.route, plugin)
        @plugin.route('foo')
        def view():
            pass
        plugin.add_url_rule.assert_called_with('foo', view, name='view', options=None)

    def test_route_decorator_name(self):
        plugin = Mock(spec=Plugin)
        plugin.route = MethodType(Plugin.route, plugin)
        @plugin.route('foo', name='bar')
        def view():
            pass
        plugin.add_url_rule.assert_called_with('foo', view, name='bar', options=None)

    def test_route_decorator_options(self):
        plugin = Mock(spec=Plugin)
        plugin.route = MethodType(Plugin.route, plugin)
        #@plugin.route('foo', name='bar', url='http://www.xbmc.org')
        @plugin.route('foo', 'bar', {'url': 'http://www.xbmc.org'})
        def view():
            pass
        plugin.add_url_rule.assert_called_with('foo', view, name='bar', options={'url': 'http://www.xbmc.org'})


class TestAddUrlRule(TestCase):
    def test_add_url_rule(self):
        plugin = Mock(spec=Plugin)
        plugin.add_url_rule = MethodType(Plugin.add_url_rule, plugin)
        plugin._view_functions = {}
        plugin._routes = []
        
        def foo():
            pass
        plugin.add_url_rule('/', foo, 'foo')
        rule = UrlRule('/', foo, 'foo', None)
        self.assertEqual(plugin._view_functions, {'foo': rule})
        self.assertEqual(plugin._routes, [rule])

    def test_2_url_rule(self):
        plugin = Mock(spec=Plugin)
        plugin.add_url_rule = MethodType(Plugin.add_url_rule, plugin)
        plugin._view_functions = {}
        plugin._routes = []
        
        def foo():
            pass
        def bar():
            pass

        plugin.add_url_rule('/foo', foo, 'foo')
        plugin.add_url_rule('/bar', bar, 'bar')
        rule_foo = UrlRule('/foo', foo, 'foo', None)
        rule_bar = UrlRule('/bar', bar, 'bar', None)
        self.assertEqual(plugin._view_functions, {'foo': rule_foo, 'bar': rule_bar})
        self.assertEqual(plugin._routes, [rule_foo, rule_bar])

    def test_2_url_rule_same_name(self):
        plugin = Mock(spec=Plugin)
        plugin.add_url_rule = MethodType(Plugin.add_url_rule, plugin)
        plugin._view_functions = {}
        plugin._routes = []
        
        def foo():
            pass
        def bar():
            pass

        plugin.add_url_rule('/foo', foo, 'biz')
        plugin.add_url_rule('/bar', bar, 'biz')
        rule_foo = UrlRule('/foo', foo, 'biz', None)
        rule_bar = UrlRule('/bar', bar, 'biz', None)
        self.assertEqual(plugin._view_functions, {'biz': None})
        self.assertEqual(plugin._routes, [rule_foo, rule_bar])

class TestUrlFor(TestCase):
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_url_for(self, mock_load_addon_strings):
        #xbmcswift2.CLI_MODE = True
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/foo')
        def foo():
            return 'bar'
        self.assertEqual(plugin.url_for('foo'), 'plugin://plugin.id/foo')

    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_ambiguous_url(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/bar')
        @plugin.route('/foo')
        def foo():
            return 'bar'
        self.assertRaises(AmbiguousUrlException, plugin.url_for, 'foo')
    
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_not_found_url(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/foo')
        def foo():
            return 'bar'
        self.assertRaises(NotFoundException, plugin.url_for, 'bar')

    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_named_routes(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/foo', name='bar')
        def foo():
            return 'bar'
        self.assertEqual(plugin.url_for('bar'), 'plugin://plugin.id/foo')
        self.assertRaises(NotFoundException, plugin.url_for, 'foo')

    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_multi_named_routes(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/bar', name='bar')
        @plugin.route('/baz', name='baz')
        def foo():
            return 'foo'
        self.assertEqual(plugin.url_for('bar'), 'plugin://plugin.id/bar')
        self.assertEqual(plugin.url_for('baz'), 'plugin://plugin.id/baz')
        self.assertRaises(NotFoundException, plugin.url_for, 'foo')


    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_url_kws_to_qs(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/foo',)
        def foo():
            return 'bar'
        self.assertEqual(plugin.url_for('foo', foo='bar'), 'plugin://plugin.id/foo?foo=bar')

    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def test_url_for_kws(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        plugin = Plugin('Plugin Name', 'plugin.id', '.')
        @plugin.route('/<foo>',)
        def foo():
            return 'bar'
        self.assertEqual(plugin.url_for('foo', foo='bar'), 'plugin://plugin.id/bar')



class TestPluginRoutes(TestCase):
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def setUp(self, mock_load_addon_strings):
        #xbmcswift2.CLI_MODE = False
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        #sys.argv = ['plugin://plugin.id/home/', 0, '?foo=bar']
        self.plugin = Plugin('My Plugin', 'my.plugin.id', '.')
        self.plugin._parse_args()

    def test_single_route(self):
        @self.plugin.route('/') 
        def mock_view():
            return 'foo'
        self.assertEqual(self.plugin._dispatch('/'), 'foo')
        self.assertEqual(self.plugin.url_for('mock_view'), 'plugin://my.plugin.id/')

    def test_multi_routes(self):
        @self.plugin.route('/') 
        def mock_view():
            return 'foo'
        @self.plugin.route('/bar')
        def mock_view2():
            return 'bar'

        self.assertEqual(self.plugin._dispatch('/'), 'foo')
        self.assertEqual(self.plugin.url_for('mock_view'), 'plugin://my.plugin.id/')
        self.assertEqual(self.plugin._dispatch('/bar'), 'bar')
        self.assertEqual(self.plugin.url_for('mock_view2'), 'plugin://my.plugin.id/bar')

    def test_multi_route_view(self):
        @self.plugin.route('/') 
        @self.plugin.route('/bar')
        def mock_view():
            return 'foo'

        self.assertEqual(self.plugin._dispatch('/'), 'foo')
        self.assertEqual(self.plugin._dispatch('/bar'), 'foo')
        self.assertRaises(AmbiguousUrlException, self.plugin.url_for, 'mock_view')

    def test_multi_route_view_names(self):
        @self.plugin.route('/foo', name='foo') 
        @self.plugin.route('/bar', name='bar')
        def mock_view():
            return 'baz'

        self.assertEqual(self.plugin._dispatch('/foo'), 'baz')
        self.assertEqual(self.plugin._dispatch('/bar'), 'baz')
        self.assertEqual(self.plugin.url_for('foo'), 'plugin://my.plugin.id/foo')
        self.assertEqual(self.plugin.url_for('bar'), 'plugin://my.plugin.id/bar')

    def test_multi_route_keywords(self):
        @self.plugin.route('/foo/<var1>')
        def mock_view(var1):
            return var1
        @self.plugin.route('/bar/', options={'var2': 'bar'})
        def mock_view2(var2):
            return var2

        self.assertEqual(self.plugin._dispatch('/foo/baz'), 'baz')
        self.assertEqual(self.plugin.url_for('mock_view', var1='baz'), 'plugin://my.plugin.id/foo/baz')
        self.assertEqual(self.plugin._dispatch('/bar/'), 'bar')
        self.assertEqual(self.plugin.url_for('mock_view2'), 'plugin://my.plugin.id/bar/')

    def test_optional_keyword_routes(self):
        @self.plugin.route('/foo/', 'noarg', {'var1': 'bar'})
        @self.plugin.route('/foo/<var1>', '1arg')
        def mock_view(var1):
            return var1

        self.assertEqual(self.plugin._dispatch('/foo/'), 'bar')
        self.assertEqual(self.plugin.url_for('noarg'), 'plugin://my.plugin.id/foo/')
        self.assertEqual(self.plugin._dispatch('/foo/biz'), 'biz')
        self.assertEqual(self.plugin.url_for('1arg', var1='biz'), 'plugin://my.plugin.id/foo/biz')

class TestPluginModuleRoutes(TestCase):
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def setUp(self, mock_load_addon_strings):
        #xbmcswift2.CLI_MODE = False
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        #sys.argv = ['plugin://plugin.id/home/', 0, '?foo=bar']
        self.plugin = Plugin('My Plugin', 'my.plugin.id', '.')
        self.plugin._parse_args()
        self.module = Module('mymodule')
    #def setUp(self):
        #self.plugin = Plugin('My Plugin', 'my.plugin.id', __file__, strings_fn='tests/data/strings.xml')
        #self.module = Module('mymodule')

    def test_routes(self):
        @self.module.route('/')
        def mock_view():
            return 'foo'

        @self.plugin.route('/')
        def mock_view2():
            return 'bar'

        self.plugin.register_module(self.module, '/module')

        self.assertEqual(self.plugin._dispatch('/'), 'bar')
        self.assertEqual(self.plugin._dispatch('/module/'), 'foo')
        self.assertEqual(self.plugin.url_for('mock_view2'), 'plugin://my.plugin.id/')
        self.assertEqual(self.plugin.url_for('mymodule.mock_view'), 'plugin://my.plugin.id/module/')
        self.assertRaises(NotFoundException, self.plugin.url_for, 'mock_view')

        self.assertEqual(self.module.url_for('mock_view2', explicit=True), 'plugin://my.plugin.id/')
        self.assertEqual(self.module.url_for('mymodule.mock_view'), 'plugin://my.plugin.id/module/')
        self.assertEqual(self.module.url_for('mock_view'), 'plugin://my.plugin.id/module/')



class TestAddItems(TestCase):
    @patch('xbmcswift2.mockxbmc.utils.load_addon_strings')
    def setUp(self, mock_load_addon_strings):
        sys.argv = ['./addon.py', 'plugin://plugin.id/home/', '?foo=bar']
        self.plugin = Plugin('My Plugin', 'my.plugin.id', '.')
        @self.plugin.route('/videos/')
        def show_videos():
            return 'videos'
        # Mock the pluign request object since it only gets loaded upon calling
        # pluign.test or plugin.run
        self.plugin._request = Mock(spec=Request)
        self.plugin.request.handle = 0

    @patch('xbmcswift2.xbmcplugin.addDirectoryItems')
    def test_add_item(self, mock_addDirectoryItems):
        item = {'label': 'My video', 'path': 'plugin://my.plugin.id/videos/'}
        _item = self.plugin.add_items([item])

    def test_1_item(self):
        items = [
            {'label': 'My video', 'path': self.plugin.url_for('show_videos'), },
            {'label': 'My video2', 'path': self.plugin.url_for('show_videos'), },
        ]
        listitems = [ListItem.from_dict(**item) for item in items]
        items = self.plugin.add_items(items)
        self.assertEqual([items[0].get_path(), items[1].get_path()], ['plugin://my.plugin.id/videos/', 'plugin://my.plugin.id/videos/'])
