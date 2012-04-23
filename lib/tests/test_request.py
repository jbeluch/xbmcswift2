from unittest import TestCase
from xbmcswift2 import Request

class TestRequest(TestCase):
    def test_init(self):
        request = Request('plugin://my.plugin.id/home/', '0', '?foo=bar&biz=buzz')
        self.assertEqual(request.url, 'plugin://my.plugin.id/home/')
        self.assertEqual(request.handle, 0)
        self.assertEqual(request.query_string, 'foo=bar&biz=buzz')
        self.assertEqual(request.args, {'foo': ['bar'], 'biz': ['buzz']})
        self.assertEqual(request.scheme, 'plugin')
        self.assertEqual(request.netloc, 'my.plugin.id')
        self.assertEqual(request.path, '/home/')
