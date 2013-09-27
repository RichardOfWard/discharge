from jinja2 import Environment, FileSystemLoader
from .plugin import Plugin


class TemplatesPlugin(Plugin):

    def can_handle_file(self, builder, path):
        return path.endswith('.html')

    def build_file(self, builder, path):
        loader = FileSystemLoader(builder.site.location)
        env = Environment(loader=loader)
        template = env.get_template(path)
        with builder.open(path) as f:
            print path
            print template.render()
            f.write(template.render())

    def build_misc(self, builder):
        pass
