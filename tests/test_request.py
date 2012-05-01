from unittest import TestCase
from xbmcswift2 import Request

class TestRequest(TestCase):
    def test_init(self):
        request = Request('plugin://my.plugin.id/home/?foo=bar&biz=buzz', '0')
        self.assertEqual(request.url, 'plugin://my.plugin.id/home/?foo=bar&biz=buzz')
        self.assertEqual(request.handle, 0)
        self.assertEqual(request.query_string, 'foo=bar&biz=buzz')
        self.assertEqual(request.args, {'foo': ['bar'], 'biz': ['buzz']})
        self.assertEqual(request.scheme, 'plugin')
        self.assertEqual(request.netloc, 'my.plugin.id')
        self.assertEqual(request.path, '/home/')

    def test_init2(self):
        '''Bug in urlparse for the following url. The netloc is '' and
        the path is incorrectly reported as 'my.plugin.id'
        '''
        request = Request('plugin://my.plugin.id/?foo=bar&biz=buzz', '0')
        self.assertEqual(request.url, 'plugin://my.plugin.id/?foo=bar&biz=buzz')
        self.assertEqual(request.handle, 0)
        self.assertEqual(request.query_string, 'foo=bar&biz=buzz')
        self.assertEqual(request.args, {'foo': ['bar'], 'biz': ['buzz']})
        self.assertEqual(request.scheme, 'plugin')
        self.assertEqual(request.netloc, 'my.plugin.id')
        self.assertEqual(request.path, '/')

    def test_pickled_qs_args(self):
        request = Request('plugin://plugin.video.helloxbmc/?foo=I3%0A.&_pickled=foo', '0')
        self.assertEqual(request.url, 'plugin://plugin.video.helloxbmc/?foo=I3%0A.&_pickled=foo')
        self.assertEqual(request.handle, 0)
        self.assertEqual(request.query_string, 'foo=I3%0A.&_pickled=foo')
        self.assertEqual(request.args, {'foo': [3]})
        self.assertEqual(request.scheme, 'plugin')
        self.assertEqual(request.netloc, 'plugin.video.helloxbmc')
        self.assertEqual(request.path, '/')
