from discharge.plugins.jinja2_templates import Jinja2TemplatesPlugin
from discharge.plugins.markdown import MarkdownPlugin

from .base import Test


class TestMarkdownPlugin(Test):

    source_dir = 'test_plugin_markdown'

    def setup(self):
        super(TestMarkdownPlugin, self).setup()
        self.templates_plugin = Jinja2TemplatesPlugin()
        self.markdown_plugin = MarkdownPlugin()
        self.site.add_plugin(self.templates_plugin)
        self.site.add_plugin(self.markdown_plugin)
        self.site.build()

    def test_markdown_file(self):
        with open(self.build_path + '/test1.html') as f:
            assert f.read().strip() == '/test1.html: <h1>HI!</h1>'

    def test_mdown_file(self):
        with open(self.build_path + '/test2.html') as f:
            assert f.read().strip() == '/test2.html: <h1>HI!</h1>'
