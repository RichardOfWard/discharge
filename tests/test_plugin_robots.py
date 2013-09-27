from .base import Test
from discharge.plugins.robots import RobotsPlugin


class TestRobotsWithout(Test):

    site_dir = 'test_robots_without_site'

    def test_robots_file(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
        self.builder.build()
        with open(self.build_path + '/robots.txt') as f:
            assert f.read() == "User-agent: *"


class TestRobotsWith(Test):

    site_dir = 'test_robots_with_site'

    def test_robots_file(self):
        robots_plugin = RobotsPlugin()
        self.site.register_plugin(robots_plugin)
        self.builder.build()
        with open(self.build_path + '/robots.txt') as f1:
            with open(self.site_path + '/robots.txt') as f2:
                assert f1.read() == f2.read()
