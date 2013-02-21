import unittest
from xbmcswift2 import UrlRule


class TestUrls(unittest.TestCase):

    def test_make_path_qs(self):
        def view(video_id):
            pass

        rule = UrlRule('/videos/<video_id>', view, view.__name__, {})

        path_qs = rule.make_path_qs({'video_id': '24'})
        self.assertEqual(path_qs, '/videos/24')

        # allow ints
        path_qs = rule.make_path_qs({'video_id': 24})
        self.assertEqual(path_qs, '/videos/24')

    def test_make_qs(self):
        def view(video_id):
            pass

        rule = UrlRule('/videos', view, view.__name__, {})

        path_qs = rule.make_path_qs({'video_id': '24'})
        self.assertEqual(path_qs, '/videos?video_id=24')

        # allow ints
        path_qs = rule.make_path_qs({'video_id': 24})
        self.assertEqual(path_qs, '/videos?video_id=24')

class TestUrlRule(unittest.TestCase):

    def test_match_without_trailing_slash(self):
        def view():
            pass
        rule = UrlRule('/videos/', view, view.__name__, {})
        self.assertEqual((view, {}), rule.match('/videos'))

    def test_match_with_trailing_slash(self):
        def view():
            pass
        rule = UrlRule('/videos', view, view.__name__, {})
        self.assertEqual((view, {}), rule.match('/videos/'))


