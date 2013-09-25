from ..exceptions import FileExists


class RobotsPlugin(object):
    def build(self, builder, out_path):
        try:
            with builder.open(out_path + '/robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
