import jinja2

from .plugin import Plugin


class Jinja2TemplatesPlugin(Plugin):
    roles = 'handler', 'page_from_content',

    def can_handle_file(self, path):
        return path.endswith('.html')

    def add_to_site(self, site):
        super(Jinja2TemplatesPlugin, self).add_to_site(site)
        self.loader = jinja2.FileSystemLoader(self.site.source_path)
        self.env = jinja2.Environment(
            loader=self.loader,
            autoescape=True,
            undefined=jinja2.StrictUndefined,
            extensions=[
                'jinja2.ext.autoescape',
                'jinja2_highlight.HighlightExtension',
            ],
        )

    def build_file(self, path, context):
        with context.input_file(path):
            with context.output_file(path) as f:
                f.write(self.render_template(path, path).encode('utf-8'))

    def render_template(self, template_name, path, **kwargs):
        context = {
            'file_path': '/' + path.lstrip('/'),
            'base_path': self.site.base_path,
        }
        context.update(kwargs)
        template = self.env.get_template(template_name)
        return template.render(**context)

    def page_from_content(self, path, content, **kwargs):
        return self.render_template(
            '_page.html',
            path,
            content=content,
            **kwargs
        )
