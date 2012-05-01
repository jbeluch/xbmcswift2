import sys
from unittest import TestCase
from xbmcswift2.cli.app import parse_cli
from xbmcswift2.common import Modes
from contextlib import contextmanager

@contextmanager
def sys_argv(*args):
    '''A context manager to patch sys.argv with the provided args list
    and return sys.argv to the initial value upon exit.
    '''
    cached_args = sys.argv[:]
    sys.argv = list(args)
    yield
    sys.argv = cached_args


class TestConsoleFunctionality(TestCase):

    def test_no_args(self):
        with sys_argv('./addon.py'):
            opts, mode, url = parse_cli()
            self.assertEqual(opts, {})
            self.assertEqual(mode, Modes.ONCE)
            self.assertEqual(url, None)

    def test_1_arg_mode(self):
        for arg, expected_mode in [('iNteractive', Modes.INTERACTIVE),
                          ('onCe', Modes.ONCE), ('crAwl', Modes.CRAWL)]:
            with sys_argv('./addon.py', arg):
                opts, mode, url = parse_cli()
                self.assertEqual({}, opts)
                self.assertEqual(expected_mode, mode)
                self.assertEqual(None, url)

    def test_1_arg_url(self):
        expected_url = 'plugin://plugin.video.helloxbmc/'
        with sys_argv('./addon.py', expected_url):
                opts, mode, url = parse_cli()
                self.assertEqual({}, opts)
                self.assertEqual(Modes.ONCE, mode)
                self.assertEqual(expected_url, url)
