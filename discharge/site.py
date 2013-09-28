import os
import shutil

from .exceptions import FileExists, DuplicateHandlers


class Site(object):

    def __init__(self, source_path, build_path=None, base_path='/'):
        if build_path is None:
            build_path = os.path.join(source_path, '_build')

        self.source_path = source_path
        self.build_path = build_path
        self.base_path = base_path
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def input_file(self, path, mode='rb', buffering=-1):
        path = os.path.join(self.source_path, path)
        return open(path, mode, buffering)

    def output_file(self, path, mode='wb', buffering=-1):
        path = os.path.join(self.build_path, path)
        if os.path.exists(path):
            raise FileExists("File %s already exists" % path)
        return open(path, mode, buffering)

    def build(self):
        assert os.path.isdir(self.source_path), \
            "Site not found at %s" % self.source_path

        walker = os.walk(self.source_path)
        for dirpath, dirnames, filenames in walker:
            dirpath = dirpath.split(self.source_path, 1)[1]
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

            os.mkdir(os.path.join(self.build_path, dirpath))

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                handlers = [plugin for plugin in self.plugins
                            if plugin.can_handle_file(self, file_path)]

                if len(handlers) > 1:
                    raise DuplicateHandlers(
                        "Multiple handlers for file '%s': %s" % (
                            file_path,
                            repr(handlers)))
                elif len(handlers) == 1:
                    handlers[0].build_file(self, file_path)
                else:
                    with self.input_file(file_path) as src:
                        with self.output_file(file_path) as dst:
                            shutil.copyfileobj(src, dst)

        for plugin in self.plugins:
            plugin.build_misc(self)
