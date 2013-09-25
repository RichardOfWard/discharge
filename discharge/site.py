import os

from .builder import Builder


class Site(object):

    def __init__(self, site_location):
        self.site_location = site_location
        self.plugins = []

    def build(self, out_path):
        builder = Builder(self, out_path)
        os.mkdir(out_path)
        for plugin in self.plugins:
            plugin.build(builder, out_path)

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
