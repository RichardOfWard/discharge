import os

from discharge.site import Site
from discharge.exceptions import FileExists, DuplicateHandlers
from discharge.plugins.plugin import Plugin

from .base import Test


class TestCoreCopying(Test):

    source_dir = 'test_core'

    def setup(self):
        super(TestCoreCopying, self).setup()
        self.site.build()

    def test_build_path(self):
        assert os.path.isdir(self.build_path)

    def test_copied_file(self):
        with open(self.source_path + '/testfile') as f1:
            with open(self.build_path + '/testfile') as f2:
                assert f1.read() == f2.read()

    def test_copied_subdir(self):
        with open(self.source_path + '/testdir/testfile') as f1:
            with open(self.build_path + '/testdir/testfile') as f2:
                assert f1.read() == f2.read()

    def test_not_copied_hiddenfile(self):
        assert os.path.exists(self.source_path + '/_hiddenfile')
        assert not os.path.exists(self.build_path + '/_hiddenfile')

    def test_not_copied_dot_hiddenfile(self):
        assert os.path.exists(self.source_path + '/.hiddenfile')
        assert not os.path.exists(self.build_path + '/.hiddenfile')

    def test_not_copied_hiddendir(self):
        assert os.path.exists(self.source_path + '/_hiddendir')
        assert not os.path.exists(self.build_path + '/_hiddendir')

    def test_not_copied_dot_hiddendir(self):
        assert os.path.exists(self.source_path + '/.hiddendir')
        assert not os.path.exists(self.build_path + '/.hiddendir')

    def test_copied_emptydir(self):
        assert os.path.isdir(self.build_path + '/emptydir')

    def test_not_copied_hiddenfile_in_subdir(self):
        assert os.path.exists(self.source_path + '/emptydir/_hiddenfile')
        assert not os.path.exists(self.build_path + '/emptydir/_hiddenfile')

    def test_not_copied_dot_hiddenfile_in_subdir(self):
        assert os.path.exists(self.source_path + '/emptydir/.hiddenfile')
        assert not os.path.exists(self.build_path + '/emptydir/.hiddenfile')


class TestCore(Test):

    source_dir = 'test_core'

    def test_default_build_dir(self):
        site = Site(self.source_path)
        assert site.build_path == self.source_path + '/_build'

    def test_output_file_checking(self):
        os.mkdir(self.build_path)
        with self.site.output_file('test'):
            pass
        try:
            with self.site.output_file('test'):
                pass
        except FileExists:
            pass
        else:
            assert False


class EagerPlugin(Plugin):
    roles = 'handler',

    def can_handle_file(self, path):
        return True


class TestPlugins(Test):

    source_dir = 'test_core'

    def test_plugins(self):
        self.site.add_plugin(Plugin())
        self.site.build()

    def test_duplicate_plugins(self):
        plugin = Plugin()
        self.site.add_plugin(plugin)
        try:
            self.site.add_plugin(plugin)
        except ValueError:
            pass
        except:
            assert False

    def test_plugin_role_names_unique(self):
        p1 = EagerPlugin()
        p2 = EagerPlugin()
        p1.roles += tuple('asdf')
        assert p1.roles is not p2.roles

    def test_plugin_role(self):
        plugin = EagerPlugin()
        self.site.add_plugin(plugin)
        assert self.site.get_plugin_by_role('handler') is plugin

    def test_missing_plugin(self):
        self.site.add_plugin(EagerPlugin())
        try:
            self.site.get_plugin_by_role('no-such-role')
        except ValueError:
            pass
        else:
            assert False

    def test_duplicate_roles(self):
        self.site.add_plugin(EagerPlugin())
        self.site.add_plugin(EagerPlugin())
        try:
            self.site.get_plugin_by_role('handler')
        except ValueError:
            pass
        else:
            assert False

    def test_multiple_roles(self):
        self.site.add_plugin(EagerPlugin())
        self.site.add_plugin(EagerPlugin())
        plugins = self.site.get_plugins_by_role('handler')
        assert len(plugins) == 2

    def test_missing_roles(self):
        self.site.add_plugin(EagerPlugin())
        self.site.add_plugin(EagerPlugin())
        plugins = self.site.get_plugins_by_role('no-such-role')
        print self.site.plugins_by_role
        assert len(plugins) == 0

    def test_modify_roles(self):
        self.site.add_plugin(EagerPlugin())
        roles = self.site.get_plugins_by_role('handler')
        assert len(roles) == 1
        roles.append('test')
        roles = self.site.get_plugins_by_role('handler')
        assert len(roles) == 1

    def test_duplicate_file(self):
        self.site.add_plugin(EagerPlugin())
        self.site.add_plugin(EagerPlugin())
        try:
            self.site.build()
        except DuplicateHandlers:
            pass
        else:
            assert False
