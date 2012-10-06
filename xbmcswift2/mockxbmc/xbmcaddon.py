import os
from xbmcswift2.logger import log
from xbmcswift2.mockxbmc import utils


class Addon(object):

    def __init__(self, id=None):
        # In CLI mode, xbmcswift2 must be run from the root of the addon
        # directory, so we can rely on getcwd() being correct.
        addonxml = os.path.join(os.getcwd(), 'addon.xml')
        self._info = {
            'id': id or utils.get_addon_id(addonxml),
            'name': utils.get_addon_name(addonxml),
        }
        self._strings = {}
        self._settings = {}

    def getAddonInfo(self, id):
        properties = ['author', 'changelog', 'description', 'disclaimer',
            'fanart', 'icon', 'id', 'name', 'path', 'profile', 'stars', 'summary',
            'type', 'version']
        assert id in properties, '%s is not a valid property.' % id
        return self._info.get(id, 'Unavailable')

    def getLocalizedString(self, id):
        key = str(id)
        assert key in self._strings, 'id not found in English/strings.xml.'
        return self._strings[key]

    def getSetting(self, id):
        try:
            value = self._settings[id]
        except KeyError:
            log.warning('xbmcaddon.Addon.getSetting() has not been implemented'
                        ' in CLI mode.')
            value = raw_input('* Please enter a temporary value for %s: ' % id)
            self._settings[id] = value
        return value

    def setSetting(self, id, value):
        self._settings[id] = value

    def openSettings(self):
        pass
