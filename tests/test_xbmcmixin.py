import os
import tempfile
import xbmcswift2
from unittest import TestCase
from mock import Mock, patch, call
from nose.plugins.skip import SkipTest
from xbmcswift2.xbmcmixin import XBMCMixin
from xbmcswift2 import xbmc
from xbmcswift2.plugin import Plugin
from xbmcswift2.common import Modes
from xbmcswift2.listitem import ListItem
from xbmcswift2.mockxbmc.xbmcaddon import Addon
from xbmcswift2 import SortMethod


TEST_STRINGS_FN = os.path.join(os.path.dirname(__file__), 'data', 'strings.xml')


class TestMixedIn(XBMCMixin):
    storage_path = '/tmp/cache'
    if not os.path.isdir(storage_path):
       os.mkdir(storage_path)
    # TODO: use a mock with return values here
    #addon = Addon('plugin.video.helloxbmc')
    addon = Mock()
    added_items = []
    handle = 0
    _end_of_directory = False

class MixedIn(XBMCMixin):

    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


class TestXBMCMixin(TestCase):

    def setUp(self):
        self.m = TestMixedIn()

    def test_temp_fn(self):
        # TODO: This test relies on hardcoded paths, fix to limit test coverage
        # TODO: This test relies on hardcoded paths which are not the same across different OS
        #self.assertEqual('/tmp/xbmcswift2_debug/temp/temp_file', self.m.temp_fn('temp_file'))
        raise SkipTest('Test not implemented.')

    def test_get_storage(self):
        cache = self.m.get_storage('animals')
        cache['dog'] = 'woof'
        cache.close()
        cache = self.m.get_storage('animals')
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

    @patch.object(xbmc, 'Player')
    @patch('xbmcswift2.ListItem', wraps=xbmcswift2.ListItem)
    def test_play_video_dict(self, WrappedListItem, MockPlayer):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(),
                         addon=Mock(),
                         added_items=[],
                         request=Mock(),
                         info_type='pictures',
                         handle=0,
                         )

        item = {'label': 'The Ultimate Showdown', 'path': 'http://example.com/video.mp4'}
        returned = plugin.play_video(item)
        returned_item = returned[0]
        self.assertTrue(returned_item.get_played())

        WrappedListItem.from_dict.assert_called_with(
            label='The Ultimate Showdown',
            info_type='video',
            path='http://example.com/video.mp4')
        self.assertTrue(MockPlayer().play.called)

        # Check that the second arg to play was an instance of xbmc listitem
        # and not xbmcswift2.ListItem
        item_arg = MockPlayer().play.call_args[0][1]
        self.assertTrue(isinstance(item_arg, xbmcswift2.xbmcgui.ListItem))

        # TODO: Implement ListItem.__eq__
        #MockPlayer().play.assert_called_with('http://example.com/video.mp4', ListItem.from_dict(**item))

    def test_play_video_listitem(self):
        pass

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



class TestAddItems(TestCase):

    @patch('xbmcswift2.ListItem.from_dict')
    @patch('xbmcswift2.xbmcplugin.addDirectoryItems')
    def test_add_items(self, addDirectoryItems, fromDict):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(),
                         addon=Mock(),
                         added_items=[],
                         request=Mock(),
                         info_type='pictures',
                         handle=0,
                         )
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo'},
            {'label': 'Course 2', 'path': 'plugin.image.test/bar'},
        ]
        returned = plugin.add_items(items)

        # TODO: Assert actual arguments passed to the addDirectoryItems call
        assert addDirectoryItems.called 
        calls = [
            call(label='Course 1', path='plugin.image.test/foo', info_type='pictures'),
            call(label='Course 2', path='plugin.image.test/bar', info_type='pictures'),
        ]
        fromDict.assert_has_calls(calls)

        # TODO: Currently ListItems don't implement __eq__
        #list_items = [ListItem.from_dict(**item) for item in items]
        #self.assertEqual(returned, list_items)

    @patch('xbmcswift2.ListItem.from_dict')
    @patch('xbmcswift2.xbmcplugin.addDirectoryItems')
    def test_add_items_no_info_type(self, addDirectoryItems, fromDict):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(),
                         addon=Mock(),
                         added_items=[],
                         request=Mock(),
                         handle=0,
                         )
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo'}
        ]
        returned = plugin.add_items(items)

        # TODO: Assert actual arguments passed to the addDirectoryItems call
        assert addDirectoryItems.called 
        calls = [
            call(label='Course 1', path='plugin.image.test/foo', info_type='video'),
        ]
        fromDict.assert_has_calls(calls)

        # TODO: Currently ListItems don't implement __eq__
        #list_items = [ListItem.from_dict(**item) for item in items]
        #self.assertEqual(returned, list_items)

    @patch('xbmcswift2.ListItem.from_dict')
    @patch('xbmcswift2.xbmcplugin.addDirectoryItems')
    def test_add_items_item_specific_info_type(self, addDirectoryItems, fromDict):
        plugin = MixedIn(storage_path=tempfile.mkdtemp(),
                         addon=Mock(),
                         added_items=[],
                         request=Mock(),
                         handle=0,
                         info_type='pictures',
                         )
        items = [
            {'label': 'Course 1', 'path': 'plugin.image.test/foo', 'info_type': 'music'}
        ]
        returned = plugin.add_items(items)

        # TODO: Assert actual arguments passed to the addDirectoryItems call
        assert addDirectoryItems.called 
        calls = [
            call(label='Course 1', path='plugin.image.test/foo', info_type='music'),
        ]
        fromDict.assert_has_calls(calls)

        # TODO: Currently ListItems don't implement __eq__
        #list_items = [ListItem.from_dict(**item) for item in items]
        #self.assertEqual(returned, list_items)



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

        # Verify video and music work
        self.m.add_to_playlist([])
        self.m.add_to_playlist([], 'video')
        self.m.add_to_playlist([], 'music')

    @patch('xbmcswift2.ListItem', wraps=ListItem)
    def test_return_values(self, MockListItem):
        # Verify dicts are transformed into listitems
        dict_items = [
            {'label': 'Grape Stomp'},
            {'label': 'Boom Goes the Dynamite'},
        ]
        items = self.m.add_to_playlist(dict_items)

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='video'),
            call(label='Boom Goes the Dynamite', info_type='video'),
        ]
        self.assertEqual(MockListItem.from_dict.call_args_list, calls)


        ## Verify with playlist=music
        MockListItem.from_dict.reset_mock()

        dict_items = [
            {'label': 'Grape Stomp'},
            {'label': 'Boom Goes the Dynamite'},
        ]
        items = self.m.add_to_playlist(dict_items, 'music')

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='music'),
            call(label='Boom Goes the Dynamite', info_type='music'),
        ]
        self.assertEqual(MockListItem.from_dict.call_args_list, calls)

        ## Verify an item's info_dict key is not used
        MockListItem.from_dict.reset_mock()

        dict_items = [
            {'label': 'Grape Stomp', 'info_type': 'music'},
            {'label': 'Boom Goes the Dynamite', 'info_type': 'music'},
        ]
        items = self.m.add_to_playlist(dict_items, 'video')

        # Verify from_dict was called properly, defaults to info_type=video
        calls = [
            call(label='Grape Stomp', info_type='video'),
            call(label='Boom Goes the Dynamite', info_type='video'),
        ]
        self.assertEqual(MockListItem.from_dict.call_args_list, calls)

        # verify ListItems were created correctly
        for item, returned_item in zip(dict_items, items):
            assert isinstance(returned_item, ListItem)
            self.assertEqual(item['label'], returned_item.get_label())

        # Verify listitems are unchanged
        MockListItem.from_dict.reset_mock()

        listitems = [
            ListItem('Grape Stomp'),
            ListItem('Boom Goes the Dyanmite'),
        ]
        items = self.m.add_to_playlist(listitems)

        self.assertFalse(MockListItem.from_dict.called)
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
