import os
import shutil

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

    def build(self, out_path):
        assert os.path.isdir(self.site.location), \
            "Site not found at %s" % self.site.location

        walker = os.walk(self.site.location)
        for dirpath, dirnames, filenames in walker:
            dirpath = dirpath.split(self.site.location, 1)[1]
            dirpath = dirpath.strip('/\\')

            hidden_dirnames = list(
                name for name in dirnames
                if name.startswith('_')
            )
            hidden_filenames = list(
                name for name in filenames
                if name.startswith('_')
            )

            for name in hidden_dirnames:
                dirnames.remove(name)

            for name in hidden_filenames:
                filenames.remove(name)

            os.mkdir(os.path.join(out_path, dirpath))

            for filename in filenames:
                src_file_name = os.path.join(
                    self.site.location,
                    dirpath,
                    filename
                )
                dst_file_name = os.path.join(
                    out_path,
                    dirpath,
                    filename
                )
                with open(src_file_name, 'rb') as src_file:
                    with self.open(dst_file_name) as dst_file:
                        shutil.copyfileobj(src_file, dst_file)

        for plugin in self.site.plugins:
            plugin.build(self, out_path)
