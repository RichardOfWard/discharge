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

    def test_serve(self):
        p = subprocess.Popen(['discharge', 'serve'],
                             cwd=self.source_path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        pt = ProcessThread(p)
        pt.start()
        time.sleep(1)

        try:
            urllib2.urlopen('http://127.0.0.1:8000/testfile.html')
        except Exception as e:
            if p.returncode is None:
                try:
                    urllib2.urlopen('http://127.0.0.1:8000/!SHUTDOWN!')
                except:
                    pass
            pt.join()
            print pt.out
            print pt.err
            raise e
        else:
            if p.returncode is None:
                try:
                    urllib2.urlopen('http://127.0.0.1:8000/!SHUTDOWN!')
                except:
                    pass
            pt.join()


class ProcessThread(threading.Thread):
    def __init__(self, p):
        super(ProcessThread, self).__init__()
        self.p = p

    def run(self):
        self.out, self.err = self.p.communicate()
