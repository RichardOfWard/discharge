import os
from .base import Test
from discharge.plugins.robots import RobotsPlugin


class TestRobots(Test):

    def test_robots_file(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
        self.site.build(self.build_path)
        with open(self.build_path + '/robots.txt') as f:
            assert f.read() == "User-agent: *"
