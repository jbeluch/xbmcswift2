import logging
from xbmcswift2 import xbmc
from xbmcswift2 import CLI_MODE

log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# TODO: Add logging to a file as well when on CLI with lowest threshold possible
# TODO: Allow a global flag to set loggin level when dealing with XBMC
# TODO: Add -q and -v flags to CLI to quiet or enabel more verbose logging


#fh = logging.FileHandler('log_filename.txt')
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(formatter)
#log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

class XBMCFilter(object):
    python_to_xbmc = {
        'DEBUG': 'LOGDEBUG',
        'INFO': 'LOGNOTICE',
        'WARNING': 'LOGWARNING',
        'ERROR': 'LOGERROR',
        'CRITICAL': 'LOGSEVERE',
    }

    xbmc_levels = {
        'LOGDEBUG': 0,
        'LOGINFO': 1,
        'LOGNOTICE': 2,
        'LOGWARNING': 3,
        'LOGERROR': 4,
        'LOGSEVERE': 5,
        'LOGFATAL': 6,
        'LOGNONE': 7,
    }

    def filter(self, record):
        xbmc_level = XBMCFilter.xbmc_levels.get(XBMCFilter.python_to_xbmc.get(record.levelname))
        xbmc.log('xbmcswift2 - %s' % (record.msg, ), xbmc_level)

        # When running in XBMC, any logged statements will be double printed
        # since we are calling xbmc.log() explicitly. Therefore we return False
        # so every log message is filtered out and not printed again.
        if CLI_MODE:
            return True
        return False


log.addFilter(XBMCFilter())
