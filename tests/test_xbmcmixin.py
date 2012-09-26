import os
from unittest import TestCase
from mock import Mock, patch, call
from nose.plugins.skip import SkipTest
from xbmcswift2.xbmcmixin import XBMCMixin
from xbmcswift2.plugin import Plugin
from xbmcswift2.common import Modes
from xbmcswift2.listitem import ListItem
from xbmcswift2.mockxbmc.xbmcaddon import Addon
from xbmcswift2 import SortMethod


TEST_STRINGS_FN = os.path.join(os.path.dirname(__file__), 'data', 'strings.xml')


class TestMixedIn(XBMCMixin):
    cache_path = '/tmp/cache'
    if not os.path.isdir(cache_path):
       os.mkdir(cache_path)
    # TODO: use a mock with return values here
    #addon = Addon('plugin.video.helloxbmc')
    addon = Mock()
    added_items = []
    handle = 0
    _end_of_directory = False

class TestXBMCMixin(TestCase):

    def setUp(self):
        self.m = TestMixedIn()

        # set fake return value of raddon.kj

    def test_cache_fn(self):
        self.assertEqual('/tmp/cache/cached_file', self.m.cache_fn('cached_file'))

    def test_temp_fn(self):
        # TODO: This test relies on hardcoded paths, fix to limit test coverage
        # TODO: This test relies on hardcoded paths which are not the same across different OS
        #self.assertEqual('/tmp/xbmcswift2_debug/temp/temp_file', self.m.temp_fn('temp_file'))
        raise SkipTest('Test not implemented.')

    def test_get_cache(self):
        cache = self.m.get_cache('animals')
        cache['dog'] = 'woof'
        cache.close()
        cache = self.m.get_cache('animals')
        self.assertEqual(cache['dog'], 'woof')

    def test_get_string(self):
        self.m.addon.getLocalizedString.return_value = 'Hello XBMC'
        self.assertEqual('Hello XBMC', self.m.get_string('30000'))
        self.assertEqual('Hello XBMC', self.m.get_string(30000))

    @patch('xbmcswift2.xbmcplugin')
    def test_set_content(self, mock_xbmcplugin):
        self.m.set_content('movies')
        assert mock_xbmcplugin.setContent.called_with(0, 'movies')

    def test_get_setting(self):
        self.m.get_setting('username')
        assert self.m.addon.getSetting.called_with(id='username')

    def test_set_setting(self):
        self.m.set_setting('username', 'xbmc')
        assert self.m.addon.setSetting.called_with(id='username', value='xbmc')

    def test_open_settings(self):
        self.m.open_settings()
        assert self.m.addon.openSettings.called

    def test_set_resolved_url(self):
        raise SkipTest('Test not implemented.')

    def test_play_video(self):
        raise SkipTest('Test not implemented.')

    def test_add_items(self):
        raise SkipTest('Test not implemented.')

    def test_end_of_directory(self):
        raise SkipTest('Test not implemented.')

    @patch('xbmcswift2.xbmcplugin.addSortMethod')
    def test_add_sort_method(self, addSortMethod):
        plugin = TestMixedIn()

        known_values = [
            # can specify by string
            ( ('title', None), (0, 9) ),
            ( ('TiTLe', None), (0, 9) ),
            # can specify as an attr on the SortMethod class
            ( (SortMethod.TITLE, None), (0, 9) ),
            ( ('date', '%D'), (0, 3, '%D') ),
            # can specify with the actual int value
            ( (3, '%D'), (0, 3, '%D') ),
        ]

        for args, call_args_to_verify in known_values:
            plugin.add_sort_method(*args)
            addSortMethod.assert_called_with(*call_args_to_verify)

    @patch('xbmcswift2.xbmcplugin.addSortMethod')
    def test_finish(self, mockAddSortMethod):
        # TODO: Add more asserts to this test
        items = [
            {'label': 'Foo', 'path': 'http://example.com/foo'},
            {'label': 'Bar', 'path': 'http://example.com/bar'},
        ]
        plugin = TestMixedIn()
        resp = plugin.finish(items, sort_methods=['title', ('dAte', '%D'), 'label', 'mpaa_rating', SortMethod.SIZE])
        calls = [
            call(0, 9),
            call(0, 3, '%D'),
            call(0, 1),
            call(0, 28),
            call(0, 4),
        ]
        mockAddSortMethod.assert_has_calls(calls)


    @patch('xbmcswift2.xbmc.executebuiltin')
    def test_notify_defalt_name(self, mockExecutebuiltin):
        plugin = TestMixedIn()
        with patch.object(plugin.addon, 'getAddonInfo', return_value='Academic Earth') as mockGetAddonInfo:
            plugin.notify('Hello World!')
        mockExecutebuiltin.assert_called_with(
            'XBMC.Notification("Hello World!", "Academic Earth", "5000", "")'
        )

    @patch('xbmcswift2.xbmc.executebuiltin')
    def test_notify(self, mockExecutebuiltin):
        plugin = TestMixedIn()
        with patch.object(plugin.addon, 'getAddonInfo', return_value='Academic Earth') as mockGetAddonInfo:
            plugin.notify('Hello World!', 'My Title', 3000, 'http://example.com/image.png')
        mockExecutebuiltin.assert_called_with(
                'XBMC.Notification("Hello World!", "My Title", "3000", "http://example.com/image.png")'
        )


class TestAddToPlaylist(TestCase):
    @patch('xbmcswift2.xbmc.Playlist')
    def setUp(self, mock_Playlist):
        self.m = TestMixedIn()

        # Mock some things so we can verify what was called
        mock_playlist = Mock()
        mock_Playlist.return_value = mock_playlist
        self.mock_Playlist = mock_Playlist
        self.mock_playlist = mock_playlist

    def test_args(self):
        # Verify playlists
        self.assertRaises(AssertionError, self.m.add_to_playlist, [], 'invalid_playlist')

        # Verify vidoe and music work
        self.m.add_to_playlist([])
        self.m.add_to_playlist([], 'video')
        self.m.add_to_playlist([], 'music')

    def test_return_values(self):
        # Verify dicts are transformed into listitems
        dict_items = [
            {'label': 'Grape Stomp'},
            {'label': 'Boom Goes the Dynamite'},
        ]
        items = self.m.add_to_playlist(dict_items)
        for item, returned_item in zip(dict_items, items):
            assert isinstance(returned_item, ListItem)
            self.assertEqual(item['label'], returned_item.get_label())

        # Verify listitems are unchange
        listitems = [
            ListItem('Grape Stomp'),
            ListItem('Boom Goes the Dyanmite'),
        ]
        items = self.m.add_to_playlist(listitems)
        for item, returned_item in zip(listitems, items):
            self.assertEqual(item, returned_item)

        # Verify mixed lists
        # Verify listitems are unchange
        listitems = [
            ListItem('Grape Stomp'),
            {'label': 'Boom Goes the Dynamite'},
        ]
        items = self.m.add_to_playlist(listitems)
        for item, returned_item in zip(listitems, items):
            assert isinstance(returned_item, ListItem)


    def test_added_to_playlist(self):
        # TODO: not working... check mocks
        listitems = [
            ListItem('Grape Stomp'),
            ListItem('Boom Goes the Dyanmite'),
        ]
        items = self.m.add_to_playlist(listitems)
        print items
        print self.mock_playlist.add.call_args_list
        for item, call_args in zip(items, self.mock_playlist.add.call_args_list):
            self.assertEqual((item.get_path(), item.as_xbmc_listitem(), 0), call_args)

    @patch('xbmcswift2.xbmcmixin.xbmc')
    def test_get_view_mode_id(self, _xbmc):
        _xbmc.getSkinDir.return_value = 'skin.confluence'
        self.assertEqual(self.m.get_view_mode_id('thumbnail'), 500)
        self.assertEqual(self.m.get_view_mode_id('THUMBNail'), 500)
        self.assertEqual(self.m.get_view_mode_id('unknown'), None)
        _xbmc.getSkinDir.return_value = 'skin.unknown'
        self.assertEqual(self.m.get_view_mode_id('thumbnail'), None)
        self.assertEqual(self.m.get_view_mode_id('unknown'), None)

    @patch('xbmcswift2.xbmcmixin.xbmc')
    def test_set_view_mode(self, _xbmc):
        self.m.set_view_mode(500)
        _xbmc.executebuiltin.assertCalledWith('Container.SetViewMode(500)')
