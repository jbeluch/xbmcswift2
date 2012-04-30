import tempfile
import os, errno


TEMP_DIR = os.path.join(tempfile.gettempdir(), 'xbmcswift2_debug')


def _create_dir(path):
    '''Creates necessary directories for the given path or does nothing
    if the directories already exist.
    '''
    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def log(msg, level=0):
    levels = [
        'LOGDEBUG',
        'LOGINFO',
        'LOGNOTICE',
        'LOGWARNING',
        'LOGERROR',
        'LOGSEVERE',
        'LOGFATAL',
        'LOGNONE',
    ]
    #print '%s - %s' % (levels[level], msg)

def translatePath(path):
    '''Creates folders in the OS's temp directory. Doesn't touch any
    possible XBMC installation on the machine. Attempting to do as
    little work as possible to enable this function to work seamlessly.
    '''
    valid_dirs = ['xbmc', 'home', 'temp', 'masterprofile', 'profile',
        'subtitles', 'userdata', 'database', 'thumbnails', 'recordings',
        'screenshots', 'musicplaylists', 'videoplaylists', 'cdrips', 'skin',
    ]

    assert path.startswith('special://'), 'Not a valid special:// path.'
    parts = path.split('/')[2:]
    assert len(parts) > 1, 'Need at least a single root directory'
    assert parts[0] in valid_dirs, '%s is not a valid root dir.' % parts[0]

    path = TEMP_DIR
    for part in parts[:-1]:
        path = os.path.join(path, part)
        _create_dir(path)

    return os.path.join(TEMP_DIR, *parts)
