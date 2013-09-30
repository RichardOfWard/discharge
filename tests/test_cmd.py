import os
import subprocess
import urllib2
import time
import threading


class TestCmd(object):
    source_path = os.path.join(os.path.dirname(__file__), 'sites/test_cmd')

    def test_no_command(self):
        p = subprocess.Popen(['discharge'],
                             cwd=self.source_path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        assert p.wait() != 0

    def test_bad_command(self):
        p = subprocess.Popen(['discharge', 'nosuchcommand'],
                             cwd=self.source_path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        assert p.wait() != 0

    def test_build(self):
        p = subprocess.Popen(['discharge', 'build'],
                             cwd=self.source_path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        if p.returncode != 0:
            print out, err
            assert False, "discharge build failed"

        assert os.path.exists(self.source_path + '/testfile.html')
