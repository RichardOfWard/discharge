import jinja2

from .plugin import Plugin


class TemplatesPlugin(Plugin):
    roles = 'handler',

    def can_handle_file(self, path):
        return path.endswith('.html')

    def build_file(self, path):
        loader = jinja2.FileSystemLoader(self.site.source_path)
        env = jinja2.Environment(
            loader=loader,
            autoescape=True,
            undefined=jinja2.StrictUndefined,
            extensions=[
                'jinja2.ext.autoescape',
                'jinja2_highlight.HighlightExtension',
            ],
        )
        template = env.get_template(path)
        with self.site.output_file(path) as f:
            f.write(
                template.render(
                    file_path='/' + path,
                    base_path=self.site.base_path,
                )
            )

    def build_misc(self):
        pass
