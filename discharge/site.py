import os


class Site(object):

    def __init__(self, site_location):
        self.site_location = site_location
        self.plugins = []

    def build(self, out_path):
        os.mkdir(out_path)
        for plugin in self.plugins:
            plugin.build(self, out_path)

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
