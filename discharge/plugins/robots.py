from .plugin import Plugin
from ..exceptions import FileExists


class RobotsPlugin(Plugin):
    def build_misc(self, builder):
        try:
            with builder.open('robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
