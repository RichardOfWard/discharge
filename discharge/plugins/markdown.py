from __future__ import absolute_import

from markdown import markdown
from .plugin import Plugin


class MarkdownPlugin(Plugin):
    roles = 'handler',
    mdown_file_extensions = '.mdown', '.markdown'

    def can_handle_file(self, path):
        for ext in self.mdown_file_extensions:
            if path.endswith(ext):
                return True

    def build_file(self, path):
        out_path = path.rsplit('.',1)
        out_path[-1] = 'html'
        out_path = ".".join(out_path)
        page_plugin = self.site.get_plugin_by_role('page_from_content')
        with self.site.input_file(path) as src_file:
            with self.site.output_file(out_path) as dst_file:
                src = src_file.read().decode('utf-8')
                content = markdown(src)
                html = page_plugin.page_from_content(out_path, content)
                dst_file.write(html.encode('utf-8'))
