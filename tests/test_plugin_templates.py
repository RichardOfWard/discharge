from .base import Test
from discharge.plugins.templates import TemplatesPlugin


class TestTemplatesPlugin(Test):

    source_dir = 'test_templates_site'

    def setup(self):
        super(TestTemplatesPlugin, self).setup()
        templates_plugin = TemplatesPlugin()
        self.site.register_plugin(templates_plugin)
        self.site.build()

    def test_non_template(self):
        with open(self.build_path + '/test.txt') as f:
            assert f.read().strip() == '{{"test"}}'

    def test_template(self):
        with open(self.build_path + '/test.html') as f:
            assert f.read().strip() == 'test'

    def test_var_file(self):
        with open(self.build_path + '/test_var_file.html') as f:
            assert f.read().strip() == 'test_var_file.html'

    def test_excaping(self):
        with open(self.build_path + '/test_escaping.html') as f:
            assert f.read().strip() == '&lt;b&gt;HI&lt;/b&gt;'
