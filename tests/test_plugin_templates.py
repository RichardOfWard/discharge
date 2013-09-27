from .base import Test
from discharge.plugins.templates import TemplatesPlugin


class TestTemplatesPlugin(Test):

    site_dir = 'test_templates_site'

    def setup(self):
        super(TestTemplatesPlugin, self).setup()
        templates_plugin = TemplatesPlugin()
        self.site.register_plugin(templates_plugin)
        self.builder.build()

    def test_non_template(self):
        with open(self.build_path + '/test.txt') as f:
            assert f.read().strip() == '{{"test"}}'

    def test_template(self):
        with open(self.build_path + '/test.html') as f:
            assert f.read().strip() == 'test'

    def test_var_file(self):
        with open(self.build_path + '/test_var_file.html') as f:
            assert f.read().strip() == 'test_var_file.html'
