#!/usr/bin/env python
from xbmcswift2 import Plugin

PLUGIN_NAME = '{plugin_name}'
PLUGIN_ID = '{plugin_id}'

plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)


@plugin.route('/')
def index():
    item = {'label': 'Hello XBMC!'}
    return [item]


if __name__ == '__main__':
    plugin.run()
