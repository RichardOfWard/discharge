from .plugin import Plugin
from ..exceptions import FileExists


class RobotsPlugin(Plugin):
    roles = 'producer',

    def produce(self, context):
        try:
            with context.output_file('robots.txt', 'wb') as f:
                f.write("User-agent: *")
        except FileExists:
            pass
