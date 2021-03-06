import os
from jinja2.exceptions import UndefinedError

from discharge.plugins.jinja2_templates import Jinja2TemplatesPlugin
from discharge.site import Site

from .base import Test


class TestTemplatesPlugin(Test):

    source_dir = 'test_plugin_jinja2_templates'

    def setup(self):
        super(TestTemplatesPlugin, self).setup()
        self.templates_plugin = Jinja2TemplatesPlugin()
        self.site.add_plugin(self.templates_plugin)
        self.build_context = self.site.build()

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

    def test_template_logged(self):
        assert "test.html" in self.build_context.input_files

    def test_base_template_logged(self):
        assert os.path.exists(self.build_path + "/derived.html")
        assert not os.path.exists(self.build_path + "/_base.html")
        assert "_base.html" in self.build_context.input_files


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
