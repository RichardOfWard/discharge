from .plugin import Plugin
from ..exceptions import FileExists


class RobotsPlugin(Plugin):
    def build_misc(self, site):
        try:
            with site.output_file('robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
