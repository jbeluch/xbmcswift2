import os
from xbmcswift2.logger import log


class Addon(object):
    def __init__(self, id):
        self._id = id
        self._strings = {}
        self._settings = {}

    def getAddonInfo(self, id):
        properties = ['author', 'changelog', 'description', 'disclaimer',
            'fanart', 'icon', 'id', 'name', 'path', 'profile', 'stars', 'summary',
            'type', 'version']
        assert id in properties, '%s is not a valid property.' % id
        return True

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
