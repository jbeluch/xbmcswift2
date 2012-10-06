import os
from contextlib import contextmanager
import xbmcswift2


@contextmanager
def preserve_cwd(cwd):
    existing = os.getcwd()
    os.chdir(cwd)
    yield
    os.chdir(existing)


@contextmanager
def preserve_cli_mode(cli_mode):
    existing = xbmcswift2.CLI_MODE
    xbmcswift2.CLI_MODE = cli_mode
    yield
    xbmcswift2.CLI_MODE = existing
