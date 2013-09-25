import os
from .base import Test
from discharge.plugins.robots import RobotsPlugin


class TestCore(Test):

    def test_site(self):
        assert self.site

    def test_site_build(self):
        self.site.build(self.build_path)
        assert os.path.isdir(self.build_path)

    def test_plugin(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
