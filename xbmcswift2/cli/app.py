'''
in plugin.run():

detect if in CLI mode and if xbmcswift2.cli is prsent
if so:
    instead of doing normal run things
    pass plugin to a pluginrunner function in cli.app

    pluginrunner handles parsing CLI
        handles getting return values and crawling
        handels interactive
        handles testing
'''
import sys
from optparse import OptionParser
from xbmcswift2.common import Modes
from xbmcswift2.request import Request
from xbmcswift2.log import log
from xbmcswift2.cli.console import display_listitems, continue_or_quit, get_user_choice
from xbmcswift2.listitem import ListItem

def plugin_runner(plugin):
    '''Handles running a plugin from the CLI.'''
    opts, mode, url = parse_cli()
    url = url or 'plugin://%s/' % plugin.id
    handle = 0
    patch_plugin(plugin, url, handle)

    handlers = {
       #Modes.XBMC: plugin._dispatch,
       Modes.ONCE:once,
       Modes.CRAWL: crawl,
       Modes.INTERACTIVE: interactive,
   }
    request_handler = handlers[mode]
    log.debug('Dispatching %s to %s' %
              (plugin.request.path, request_handler.__name__))
    request_handler(plugin)
    #return request_handler(plugin.request.path)


def patch_plugin(plugin, path, handle=None):
    if handle is None:
        handle = plugin.request.handle
    plugin._request = Request(path, handle)

def once(plugin, parent_item=None):
    plugin.clear_added_items()
    items = plugin._dispatch(plugin.request.path)

    # Prepend the parent_item if given
    if parent_item is not None:
        items.insert(0, parent_item)

    display_listitems(items)
    return items


# TODO: clear plugin's listitem state
def interactive(plugin):
    items = [item for item in once(plugin) if not item.get_played()]
    parent_stack = []  # Keep track of parents so we can have a '..' option

    selected_item = get_user_choice(items)
    while selected_item is not None:
        if parent_stack and selected_item == parent_stack[-1]:
            # User selected the parent item, remove from list
            parent_stack.pop()
        else:
            # User selected non parent item, add current url to parent stack
            parent_stack.append(ListItem.from_dict(label='..',
                                                   path=plugin.request.url))
        patch_plugin(plugin, selected_item.get_path())

        # If we have parent items, include the top of the stack in the list
        # item display
        parent_item = None
        if parent_stack:
            parent_item = parent_stack[-1]
        items = [item for item in once(plugin, parent_item=parent_item)
                 if not item.get_played()]
        selected_item = get_user_choice(items)


def crawl(plugin):
    '''Performs a breadth-first crawl of all possible routes from the
    starting path. Will only visit a URL once, even if it is referenced
    multiple times in a plugin. Requires user interaction in between each
    fetch.
    '''
    # TODO: use OrderedSet?
    paths_visited = set()
    paths_to_visit = set(item.get_path() for item in once(plugin))

    while paths_to_visit and continue_or_quit():
        path = paths_to_visit.pop()
        paths_visited.add(path)

        # Run the new listitem
        patch_plugin(plugin, path)
        new_paths = set(item.get_path() for item in once(plugin))

        # Filter new items by checking against urls_visited and
        # urls_tovisit
        paths_to_visit.update(path for path in new_paths
                              if path not in paths_visited)


def parse_cli():
    '''Command line interface for xbmcswift.'''
    parser = OptionParser()
    parser.description = parse_cli.__doc__
    #parser.set_usage(USAGE)

    #parser.add_option('-q', '--quiet', action='store_true')
    #parser.add_option('-v', '--verbose', action='store_true')
    #parser.add_option('-V', '--version', action='store_true')

    opts, args = parser.parse_args()

    mode = Modes.ONCE
    if len(args) > 0 and hasattr(Modes, args[0].upper()):
        _mode = args.pop(0).upper()
        mode = getattr(Modes, _mode)

    url = None
    if len(args) > 0:
        # A url was specified
        url = args.pop(0)

    return opts, mode, url
