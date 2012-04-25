from xbmcswift2.common import unpickle_dict
from urlparse import urlparse
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs


class Request(object):
    # TODO: no need for a class?

    def __init__(self, url, handle, query_string):
        # TODO: combine argv0 and argtv1 then use urlparse to get the query
        # string before passing to parse_qs
        self.url = url
        self.handle = int(handle)
        self.query_string = query_string.lstrip('?')
        self.args = unpickle_dict(parse_qs(self.query_string))

        # urlparse doesn't like the 'plugin' scheme, so pass a protocol
        # relative url, e.g. //plugin.video.helloxbmc/path
        self.scheme, remainder = url.split(':', 1)
        parts = urlparse(remainder)
        _, self.netloc, self.path = parts[0], parts[1], parts[2]
