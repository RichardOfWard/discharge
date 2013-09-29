from .plugin import Plugin
from ..exceptions import FileExists


class RobotsPlugin(Plugin):
    roles = 'producer',

    def produce(self):
        try:
            with self.site.output_file('robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
