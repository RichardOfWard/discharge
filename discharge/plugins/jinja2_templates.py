import os
import jinja2
from .plugin import Plugin
from .jinja2_filters.highlight import highlight_filter


class TrackingFileSystemLoader(jinja2.FileSystemLoader):
    def __init__(self, *args, **kwargs):
        self._context = None
        super(TrackingFileSystemLoader,
              self).__init__(*args, **kwargs)

    def get_source(self, environment, template):
        pieces = jinja2.loaders.split_template_path(template)
        self._context.input_files.add(os.path.join(*pieces))
        return super(TrackingFileSystemLoader,
                     self).get_source(environment, template)


class Jinja2TemplatesPlugin(Plugin):
    roles = 'handler', 'page_from_content',
    extensions = ['jinja2.ext.autoescape']
    autoescape = True
    filters = {'highlight': highlight_filter}

    def can_handle_file(self, path):
        return path.endswith('.html')

    def add_to_site(self, site):
        super(Jinja2TemplatesPlugin, self).add_to_site(site)
        self.loader = TrackingFileSystemLoader(self.site.source_path)
        self.env = jinja2.Environment(
            loader=self.loader,
            autoescape=self.autoescape,
            undefined=jinja2.StrictUndefined,
            extensions=self.extensions,
        )
        for name, func in self.filters.items():
            self.env.filters[name] = func

    def build_file(self, path, context):
        with context.input_file(path):
            with context.output_file(path) as f:
                f.write(self.render_template(path, path, context).encode('utf-8'))

    def render_template(self, template_name, path, context, **kwargs):
        template_context = {
            'file_path': '/' + path.lstrip('/'),
            'base_path': self.site.base_path,
        }
        template_context.update(kwargs)
        self.loader._context = context
        template = self.env.get_template(template_name)
        return template.render(**template_context)

    def page_from_content(self, path, content, context, **kwargs):
        return self.render_template(
            '_page.html',
            path,
            context,
            content=content,
            **kwargs
        )
