from jinja2 import Environment, FileSystemLoader
from .plugin import Plugin


class TemplatesPlugin(Plugin):

    def can_handle_file(self, site, path):
        return path.endswith('.html')

    def build_file(self, site, path):
        loader = FileSystemLoader(site.source_path)
        env = Environment(
            loader=loader,
            autoescape=True,
            extensions=[
                'jinja2.ext.autoescape',
                'jinja2_highlight.HighlightExtension',
            ]
        )
        template = env.get_template(path)
        with site.output_file(path) as f:
            f.write(
                template.render(
                    file=path,
                    base_path=site.base_path
                )
            )

    def build_misc(self, site):
        pass
