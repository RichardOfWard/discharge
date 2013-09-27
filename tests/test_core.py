import os
from .base import Test
from discharge.builder import Builder
from discharge.exceptions import FileExists, DuplicateHandlers
from discharge.plugins.plugin import Plugin

class EagerPlugin(Plugin):
    def can_handle_file(self, builder, path):
        return True

class TestCoreCopying(Test):

    site_dir = 'test_core_site'

    def setup(self):
        super(TestCoreCopying, self).setup()
        self.builder.build()

    def test_build_path(self):
        assert os.path.isdir(self.build_path)
        
    def test_copied_file(self):
        with open(self.site_path + '/testfile') as f1:
            with open(self.build_path + '/testfile') as f2:
                assert f1.read() == f2.read()

    def test_copied_subdir(self):
        with open(self.site_path + '/testdir/testfile') as f1:
            with open(self.build_path + '/testdir/testfile') as f2:
                assert f1.read() == f2.read()

    def test_not_copied_hiddendir(self):
        assert not os.path.exists(self.build_path + '/_hiddendir')

    def test_copied_emptydir(self):
        assert os.path.isdir(self.build_path + '/emptydir')

    def test_not_copied_emptyfile(self):
        assert not os.path.exists(self.build_path + '/emptydir/_hiddenfile')

class TestCore(Test):

    site_dir = 'test_core_site'

    def test_output_file_checking(self):
        os.mkdir(self.build_path)
        with self.builder.open('test'):
            pass
        try:
            with self.builder.open('test'):
                pass
        except FileExists:
            pass
        else:
            assert False

    def test_plugins(self):
        self.site.register_plugin(Plugin())
        self.builder.build()

    def test_duplicate_handlers(self):
        self.site.register_plugin(EagerPlugin())
        self.site.register_plugin(EagerPlugin())
        try:
            self.builder.build()
        except DuplicateHandlers:
            pass
        else:
            assert  False
