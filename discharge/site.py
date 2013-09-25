import os
import shutil

from .builder import Builder


class Site(object):

    def __init__(self, site_location):
        self.site_location = site_location
        self.plugins = []

    def build(self, out_path):
        assert os.path.isdir(self.site_location), \
            "Site not found at %s" % self.site_location

        builder = Builder(self, out_path)
        walker = os.walk(self.site_location)
        for dirpath, dirnames, filenames in walker:
            dirpath = dirpath.split(self.site_location, 1)[1]
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
                    self.site_location,
                    dirpath,
                    filename
                )
                dst_file_name = os.path.join(
                    out_path,
                    dirpath,
                    filename
                )
                with open(src_file_name, 'rb') as src_file:
                    with builder.open(dst_file_name) as dst_file:
                        shutil.copyfileobj(src_file, dst_file)

        for plugin in self.plugins:
            plugin.build(builder, out_path)

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
