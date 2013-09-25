import os
from .base import Test
from discharge.builder import Builder
from discharge.exceptions import FileExists

class TestCore(Test):

    def test_site(self):
        assert self.site

    def test_site_build(self):
        self.site.build(self.build_path)
        assert os.path.isdir(self.build_path)

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
