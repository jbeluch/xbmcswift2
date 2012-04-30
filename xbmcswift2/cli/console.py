'''
    xbmcswift2.console
    ------------------

    This module contains code to handle CLI interaction.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
from optparse import OptionParser
from xbmcswift2.common import Modes


def display_listitems(items):
    '''Prints a list of items along with the current index'''
    print '--'
    for i, item in enumerate(items):
        print '[%d] %s' % (i, item)


def display_video(item):
    '''Prints a message for playing a video'''
    print '--'
    print '[Playing Video] %s' % item


def get_user_choice(items):
    '''Returns the selected item from provided items or None if 'q' was
    entered for quit.
    '''
    choice = raw_input('Choose an item or "q" to quit: ')
    while choice != 'q':
        try:
            return items[int(choice)]
        except ValueError:
            # Passed something that cound't be converted with int()
            choice = raw_input('You entered a non-integer. Choice must be an'
                               ' integer or "q": ')
        except IndexError:
            # Passed an integer that was out of range of the list of urls
            choice = raw_input('You entered an invalid integer. Choice must be'
                               ' from above url list or "q": ')
    return None


def continue_or_quit():
    '''Prints an exit message and returns False if the user wants to
    quit.
    '''
    return raw_input('Enter to continue or "q" to quit') != 'q'


