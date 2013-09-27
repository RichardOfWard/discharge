import os
import shutil

from .exceptions import FileExists, DuplicateHandlers


class Builder(object):
    def __init__(self, site, out_path):
        self.site = site
        self.out_path = out_path

    def open(self, path, mode='wb', buffering=-1):
        path = os.path.join(self.out_path, path)
        if os.path.exists(path):
            raise FileExists("File %s already exists" % path)
        return open(path, mode, buffering)

    def build(self):
        assert os.path.isdir(self.site.location), \
            "Site not found at %s" % self.site.location

        walker = os.walk(self.site.location)
        for dirpath, dirnames, filenames in walker:
            dirpath = dirpath.split(self.site.location, 1)[1]
            dirpath = dirpath.strip('/\\')

            hidden_dirnames = list(
                name for name in dirnames
                if name.startswith('_') or name.startswith('.')
            )
            hidden_filenames = list(
                name for name in filenames
                if name.startswith('_') or name.startswith('.')
            )

            for name in hidden_dirnames:
                dirnames.remove(name)

            for name in hidden_filenames:
                filenames.remove(name)

            os.mkdir(os.path.join(self.out_path, dirpath))

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                handlers = [plugin for plugin in self.site.plugins
                            if plugin.can_handle_file(self, file_path)]

                if len(handlers) > 1:
                    raise DuplicateHandlers(
                        "Multiple handlers for file '%s': %s" % (
                            file_path,
                            repr(handlers)))
                elif len(handlers) == 1:
                    handlers[0].build_file(self, file_path)
                else:
                    src_file_path = os.path.join(self.site.location, file_path)
                    dst_file_path = os.path.join(self.out_path, file_path)
                    with open(src_file_path, 'rb') as src_file:
                        with self.open(dst_file_path) as dst_file:
                            shutil.copyfileobj(src_file, dst_file)

        for plugin in self.site.plugins:
            plugin.build_misc(self)
