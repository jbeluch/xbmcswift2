import unittest
import tempfile
from xbmcswift2.cli import create


class TestCreate(unittest.TestCase):

    def test_update_regular_file(self):
        fileobj, filename = tempfile.mkstemp(suffix='.py', text=True)

        # setup
        with open(filename, 'w') as fileobj:
            fileobj.write('This is a test of the emergency {broadcast} system.')

        create.update_file(filename, {'broadcast': 'kitten'})

        with open(filename, 'r') as fileobj:
            result = fileobj.read()
        self.assertEqual('This is a test of the emergency kitten system.', result)

    def test_update_xml_file(self):
        fileobj, filename = tempfile.mkstemp(suffix='.xml', text=True)
        print filename

        # setup
        with open(filename, 'w') as fileobj:
            fileobj.write('<tag provider={provider}/>')

        create.update_file(filename, {'provider': 'name aka "another name" <name@domain.com> \'foo\''})

        with open(filename, 'r') as fileobj:
            result = fileobj.read()
        expected = '<tag provider="name aka &quot;another name&quot; &lt;name@domain.com&gt; \'foo\'"/>'
        self.assertEqual(expected, result)
