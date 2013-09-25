class RobotsPlugin(object):
    def build(self, builder, out_path):
        with builder.open(out_path + '/robots.txt', 'wb') as f:
            f.write("User-agent: *")
