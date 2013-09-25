class RobotsPlugin(object):
    def build(self, site, out_path):
        with open(out_path + '/robots.txt', 'wb') as f:
            f.write("User-agent: *")
