import unittest
from xbmcswift2.cli import console


class TestConsole(unittest.TestCase):

    def test_get_max_len(self):
        items = ['a', 'bb', 'ccc', 'dddd']
        self.assertEqual(console.get_max_len(items), 4)
        self.assertEqual(console.get_max_len([]), 0)
