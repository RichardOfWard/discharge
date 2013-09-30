from __future__ import absolute_import

from markdown import Markdown
from .plugin import Plugin


class MarkdownPlugin(Plugin):
    roles = 'handler',
    markdown_file_extensions = '.mdown', '.markdown'
    markdown_extensions = 'extra', 'meta'

    def can_handle_file(self, path):
        for ext in self.markdown_file_extensions:
            if path.endswith(ext):
                return True

    def build_file(self, path, context):
        out_path = path.rsplit('.', 1)
        out_path[-1] = 'html'
        out_path = ".".join(out_path)
        page_plugin = self.site.get_plugin_by_role('page_from_content')
        with context.input_file(path) as src_file:
            with context.output_file(out_path) as dst_file:
                src = src_file.read().decode('utf-8')
                md = Markdown(
                    extensions=self.markdown_extensions,
                )
                content = md.convert(src)
                meta = {'title': ''}
                meta.update(md.Meta)
                html = page_plugin.page_from_content(
                    out_path,
                    content,
                    **meta
                )
                dst_file.write(html.encode('utf-8'))
