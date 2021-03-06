import os
import tempfile
import shutil

from discharge.site import Site


class Test(object):
    def setup(self):
        self.source_path = os.path.join(
            os.path.dirname(__file__),
            'sites/',
            self.source_dir,
        )
        self.build_path_container = tempfile.mkdtemp()
        self.build_path = self.build_path_container + '/build'
        self.site = Site(self.source_path, self.build_path)

    def teardown(self):
        shutil.rmtree(self.build_path_container)
