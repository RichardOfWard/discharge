import os

from .exceptions import FileExists


class BuildContext(object):
    def __init__(self, site):
        self.site = site
        self.input_files = set()

    def input_file(self, path, mode='rb', buffering=-1):
        path = os.path.join(self.site.source_path, path)
        f = open(path, mode, buffering)
        self.input_files.add(path)
        return f

    def output_file(self, path, mode='wb', buffering=-1):
        path = os.path.join(self.site.build_path, path)
        if os.path.exists(path):
            raise FileExists("File %s already exists" % path)
        return open(path, mode, buffering)
