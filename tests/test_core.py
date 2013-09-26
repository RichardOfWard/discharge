import os
from .base import Test
from discharge.builder import Builder
from discharge.exceptions import FileExists


class TestCoreCopying(Test):

    site_dir = 'test_core_site'

    def setup(self):
        super(TestCoreCopying, self).setup()
        self.builder.build(self.build_path)

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


class TestCoreFileChecking(Test):

    site_dir = 'test_core_site'

    def test_output_file_checking(self):
        builder = Builder(self.site, self.build_path)
        os.mkdir(self.build_path)
        with builder.open('test'):
            pass
        try:
            with builder.open('test'):
                pass
        except FileExists:
            pass
        else:
            assert False
