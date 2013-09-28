from .base import Test
from discharge.plugins.templates import TemplatesPlugin

from discharge.site import Site


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

    def test_escaping(self):
        with open(self.build_path + '/test_escaping.html') as f:
            assert f.read().strip() == '&lt;b&gt;HI&lt;/b&gt;'

    def test_var_file(self):
        with open(self.build_path + '/test_var_file.html') as f:
            assert f.read().strip() == 'test_var_file.html'

    def test_var_base_path(self):
        with open(self.build_path + '/test_var_base_path.html') as f:
            assert f.read().strip() == '/'


class TestTemplatesPlugin2(Test):

    source_dir = 'test_templates_site'

    def setup(self):
        super(TestTemplatesPlugin2, self).setup()
        self.site = Site(self.source_path, self.build_path, '/foo/')
        templates_plugin = TemplatesPlugin()
        self.site.register_plugin(templates_plugin)
        self.site.build()

    def test_var_base_path(self):
        with open(self.build_path + '/test_var_base_path.html') as f:
            assert f.read().strip() == '/foo/'
