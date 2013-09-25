import os
import tempfile
import shutil

from discharge.site import Site


class Test(object):
    def setup(self):
        self.site_path = os.path.dirname(__file__)+'/test_site'
        self.build_path_container = tempfile.mkdtemp()
        self.build_path = self.build_path_container + '/build'
        self.site = Site(self.site_path)

    def teardown(self):
        shutil.rmtree(self.build_path_container)
