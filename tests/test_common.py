from unittest import TestCase
from xbmcswift2.common import xbmc_url, enum, clean_dict, pickle_dict, unpickle_dict, unhex


class TestXBMCUrl(TestCase):
    def test_xbmc_url(self):
        known_values = (
            # url, options_dict, expected_value
            ('url', {}, 'url'),
            ('url', {'key': 'val'}, 'url key=val'),
            ('url', {'key': 3}, 'url key=3'),
            ('url', {'a': 'b', 'c': 'd'}, 'url a=b c=d'),
        )
        for url, options, expected in known_values:
            self.assertEqual(expected, xbmc_url(url, **options))

class TestEnum(TestCase):
    def test_kwargs_enum(self):
        States = enum(NJ='New Jersey', NY='New York')
        self.assertEqual(States.NJ, 'New Jersey')
        self.assertEqual(States.NY, 'New York')
        self.assertEqual(sorted(States._fields), sorted(['NJ', 'NY']))

    def test_args_enum(self):
        States = enum('NEW_JERSEY', 'NEW_YORK')
        self.assertEqual(States.NEW_YORK, 'NEW_YORK')
        self.assertEqual(States.NEW_JERSEY, 'NEW_JERSEY')
        self.assertEqual(sorted(States._fields), sorted(['NEW_YORK', 'NEW_JERSEY']))

    def test_mixed_enum(self):
        States = enum('NEW_JERSEY', NY='NEW_YORK')
        self.assertEqual(States.NY, 'NEW_YORK')
        self.assertEqual(States.NEW_JERSEY, 'NEW_JERSEY')
        self.assertEqual(sorted(States._fields), sorted(['NY', 'NEW_JERSEY']))

#class TestUrlParse(TestCase):
    #def test_url_parse(self):
        ## supposed to return scheme, netloc and path 
        #known_values = (
            ## url, scheme, netloc, path
            #('plugin://my.plugin.id/path/', 'plugin', 'my.plugin.id', '/path/'),
            #('plugin://my.plugin.id:8080/path/', 'plugin', 'my.plugin.id:8080', '/path/'),
            #('plugin://my.plugin.id:8080/', 'plugin', 'my.plugin.id:8080', '/'),
            #('http://my.plugin.id/path?foo=bar', 'http', 'my.plugin.id', '/path?foo=bar'),
            #('http://example.com/path/to/video', 'http', 'example.com', '/path/to/video'),
        #)
        #for url, netloc, scheme, path in known_values:
            #self.assertEqual(urlparse(url), (netloc, scheme, path))

class TestCleanDict(TestCase):
    def test_clean_dict(self):
       items = { 'foo': 'foo', 'bar': None, 'baz': False, 'age': 0, }
       expected = { 'foo': 'foo', 'baz': False, 'age': 0, }
       self.assertEqual(expected, clean_dict(items))


class TestPickleDict(TestCase):
    def test_pickle_dict(self):
        items = {
            'name': u'jon',
            'animal': 'dog',
            'boolean': True,
            'number': 42,
            'list': ['a', 'b'],
            'dict': {'foo': 'bar'},
        }
        pickled = pickle_dict(items)
        expected = (
            ('name', u'jon'),
            ('animal', 'dog'),
            ('boolean', 'I01\n.'),
            ('number', 'I42\n.'),
            ('list', "(lp0\nS'a'\np1\naS'b'\np2\na."),
            ('dict', "(dp0\nS'foo'\np1\nS'bar'\np2\ns."),
        )


        self.assertEqual(len(pickled.items()), 7)
        for key, val in expected:
            self.assertEqual(pickled.get(key), val)
        fields = pickled.get('_pickled').split(',')
        self.assertEqual(sorted(fields), ['boolean', 'dict', 'list', 'number'])
        self.assertEqual(unpickle_dict(pickled), items)
        self.assertEqual(unpickle_dict(pickle_dict(items)), items)


class TestDownloadPage(TestCase):
    def test_download_page(self):
        pass


class TestUnhex(TestCase):
    def test_unhex(self):
        known_values = (
            ('\x20', ' '),
            ('\x3d\x20', '= '),
            ('\x3D\x20', '= '),
        )

        for hexed, unhexed in known_values:
            self.assertEqual(unhexed, unhex(hexed))
