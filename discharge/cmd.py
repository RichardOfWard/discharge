import os
import sys

from discharge.exceptions import UsageError


def do_cmd():
    try:
        if len(sys.argv) < 2:
            raise UsageError()
        elif len(sys.argv) == 2 and sys.argv[1] == 'build':
            site = load_site_config()
            site.build()
        elif len(sys.argv) == 2 and sys.argv[1] == 'serve':
            site = load_site_config()
            from discharge.server import Server
            Server(site, use_reloader=True).run()
        else:
            raise UsageError()
    except UsageError:
        print "Usage:"
        print "discharge [command]"
        print "where command is one of: build, serve"
        sys.exit(1)


def load_site_config():
    settings_file = "_discharge.py"
    dct = {'__file__': os.path.realpath('_discharge.py')}
    execfile(settings_file, dct)
    return dct['site']
