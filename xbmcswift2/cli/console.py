'''
    xbmcswift2.console
    ------------------

    This module contains code to handle CLI interaction.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
from optparse import OptionParser
from xbmcswift2.common import Modes


def get_max_len(items):
    '''Returns the max of the lengths for the provided items'''
    return max(len(item) for item in items)


def display_listitems(items):
    '''Prints a list of items along with the current index'''
    label_width = get_max_len(item.get_label() for item in items)
    num_width = len(str(len(items)))
    output = []
    for i, item in enumerate(items):
        output.append('[%s] %s (%s)' % (
            str(i).rjust(num_width),
            item.get_label().ljust(label_width),
            item.get_path()))

    line_width = get_max_len(output)
    output.append('-' * line_width)

    header = [
        '-' * line_width,
        '%s %s Path' % ('#'.center(num_width + 2), 'Label'.ljust(label_width)),
        '-' * line_width,
    ]
    print '\n'.join(header + output)


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
