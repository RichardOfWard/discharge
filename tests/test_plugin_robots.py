from .base import Test
from discharge.plugins.robots import RobotsPlugin


class TestRobotsWithout(Test):

    source_dir = 'test_plugin_robots_without'

    def test_robots_file(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
        self.site.build()
        with open(self.build_path + '/robots.txt') as f:
            assert f.read() == "User-agent: *"


class TestRobotsWith(Test):

    source_dir = 'test_plugin_robots_with'

    def test_robots_file(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
        self.site.build()
        with open(self.build_path + '/robots.txt') as f1:
            with open(self.source_path + '/robots.txt') as f2:
                assert f1.read() == f2.read()
