class Site(object):

    def __init__(self, location):
        self.location = location
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
