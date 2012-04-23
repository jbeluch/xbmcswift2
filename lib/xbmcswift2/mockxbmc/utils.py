from xml.dom.minidom import parse

def load_addon_strings(addon, filename):
    '''This is not an official XBMC method, it is here to faciliate
    mocking up the other methods when running outside of XBMC.'''
    def get_strings(fn):
        xml = parse(fn)
        strings = dict((tag.getAttribute('id'), tag.firstChild.data) for tag in xml.getElementsByTagName('string'))
        #strings = {}
        #for tag in xml.getElementsByTagName('string'):
            #strings[tag.getAttribute('id')] = tag.firstChild.data
        return strings
    addon._strings = get_strings(filename)
