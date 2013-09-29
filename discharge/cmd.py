import os
import sys

from discharge.exceptions import UsageError


def load_site_config():
    settings_file = "_discharge.py"
    dct = {'__file__': os.path.realpath('_discharge.py')}
    execfile(settings_file, dct)
    return dct['site']


def do_cmd():
    try:
        if len(sys.argv) < 2:
            raise UsageError()
        if len(sys.argv) == 2 and sys.argv[1] == 'build':
            site = load_site_config()
            site.build()
        else:
            raise UsageError()
    except UsageError:
        print "Usage:"
        print "discharge [command]"
        print "where command is one of:"
        print "    build"
        sys.exit(1)
