import os

class Addon(object):
    def __init__(self, id):
        self._id = id
        self._strings = {}

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
        raise NotImplementedError, 'Not ready yet!'

    def setSetting(self, id, value):
        raise NotImplementedError, 'Not ready yet!'

    def openSettings(self):
        pass

