import os

from .exceptions import FileExists


class Builder(object):
    def __init__(self, site, out_path):
        self.site = site
        self.out_path = out_path

    def open(self, path, mode='wb', buffering=-1):
        path = os.path.join(self.out_path, path)
        if os.path.exists(path):
            raise FileExists("File %s already exists" % path)
        return open(path, mode, buffering)

