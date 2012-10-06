import unittest
from xbmcswift2 import SortMethod


class TestSortMethod(unittest.TestCase):

    def test_from_string(self):
        known_values = [
            ('title', 9),
            ('TiTLe', 9),
            ('label', 1),
            ('LAbel', 1),
        ]
        for sort_method, value in known_values:
            self.assertEqual(SortMethod.from_string(sort_method), value)

    def test_attrs(self):
        known_values = [
            ('TITLE', 9),
            ('DATE', 3),
            ('LABEL_IGNORE_THE', 2),
        ]

        for sort_method, value in known_values:
            self.assertEqual(getattr(SortMethod, sort_method), value)
