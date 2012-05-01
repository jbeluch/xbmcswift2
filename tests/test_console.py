from unittest import TestCase
from xbmcswift2.cli.console import parse_cli
from xbmcswift2.common import Modes

PLUGIN_ID = 'plugin.video.helloxbmc'
class ParseCommandLine(TestCase):
    def test_noargs(self):
       # When run from the command line, we ignore the first arg as it is the program name
       args = []
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

    def test_onearg_modes(self):
       # once
       args = ['once']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

       # crawl
       args = ['crawl']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.CRAWL, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

       # interactive
       args = ['interactive']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.INTERACTIVE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

       # xbmc
       args = ['xbmc']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.XBMC, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)


    def test_mode_case(self):
       # once
       args = ['OncE']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

    def test_twoargs(self):
       # [mode, url]
       args = ['once', 'plugin://plugin.video.helloxbmc/videos/']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/videos/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

       args = ['crawl', 'plugin://plugin.video.helloxbmc/videos/']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.CRAWL, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/videos/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?', query_string)

       # [url, query_string]
       args = ['plugin://plugin.video.helloxbmc/videos/', '?foo=bar&frog=toad']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/videos/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?foo=bar&frog=toad', query_string)

    def test_threeargs(self):
       # [mode, url, query_string]
       args = ['once', 'plugin://plugin.video.helloxbmc/videos/', '?foo=bar&frog=toad']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.ONCE, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/videos/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?foo=bar&frog=toad', query_string)

       args = ['CRAWL', 'plugin://plugin.video.helloxbmc/videos/', '?foo=bar&frog=toad']
       mode, [url, handle, query_string] = parse_cli(args, PLUGIN_ID)
       self.assertEqual(Modes.CRAWL, mode)
       self.assertEqual('plugin://plugin.video.helloxbmc/videos/', url)
       self.assertEqual('0', handle)
       self.assertEqual('?foo=bar&frog=toad', query_string)

