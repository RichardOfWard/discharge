from .plugin import Plugin
from ..exceptions import FileExists


class RobotsPlugin(Plugin):
    def build_misc(self, builder):
        try:
            with builder.open(builder.out_path + '/robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
