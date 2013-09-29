from jinja2.exceptions import UndefinedError

from discharge.plugins.jinja2_templates import Jinja2TemplatesPlugin
from discharge.site import Site

from .base import Test


class TestTemplatesPlugin(Test):

    source_dir = 'test_plugin_jinja2_templates'

    def setup(self):
        super(TestTemplatesPlugin, self).setup()
        templates_plugin = Jinja2TemplatesPlugin()
        self.site.add_plugin(templates_plugin)
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
            assert f.read().strip() == '/test_var_file.html'

    def test_var_base_path(self):
        with open(self.build_path + '/test_var_base_path.html') as f:
            assert f.read().strip() == ''

    def test_pygments(self):
        with open(self.build_path + '/test_pygments.html') as f:
            assert f.read().strip() == (
                """<div class="highlight"><pre><span class="kn">import"""
                """</span> <span class="nn">love</span>\n"""
                """</pre></div>"""
            )


class TestTemplatesPluginBasePath(Test):

    source_dir = 'test_plugin_jinja2_templates'

    def setup(self):
        super(TestTemplatesPluginBasePath, self).setup()
        self.site = Site(self.source_path, self.build_path, '/foo')
        templates_plugin = Jinja2TemplatesPlugin()
        self.site.add_plugin(templates_plugin)
        self.site.build()

    def test_var_base_path(self):
        with open(self.build_path + '/test_var_base_path.html') as f:
            assert f.read().strip() == '/foo'


class TestTemplatesPluginUndefined(Test):

    source_dir = 'test_plugin_jinja2_templates_undefined'

    def setup(self):
        super(TestTemplatesPluginUndefined, self).setup()
        self.site = Site(self.source_path, self.build_path, '/foo')
        templates_plugin = Jinja2TemplatesPlugin()
        self.site.add_plugin(templates_plugin)

    def test_undefined(self):
        try:
            self.site.build()
        except UndefinedError:
            pass
        else:
            assert False, "Undefined variable raised no exception"
