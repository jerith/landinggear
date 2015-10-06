from __future__ import absolute_import, print_function

import os
from contextlib import contextmanager
from shutil import rmtree
from tempfile import mkdtemp


@contextmanager
def tempdir(suffix="", prefix="tmp", dir=None):
    tmpdir_path = mkdtemp(suffix, prefix, dir)
    try:
        yield tmpdir_path
    finally:
        rmtree(tmpdir_path)


@contextmanager
def tempcache():
    with tempdir() as basedir:
        yield TempPipCache(os.path.join(basedir, "pipcache"))


class TempPipCache(object):
    def __init__(self, pip_cache_dir):
        self.path = pip_cache_dir
        os.mkdir(self.path)
        os.mkdir(self.join("http"))
        os.mkdir(self.join("wheels"))

    def join(self, *pathbits):
        return os.path.join(self.path, *pathbits)

    def write_file(self, filepath, content=b""):
        fullpath = self.join(*filepath.split("/"))
        os.makedirs(os.path.dirname(fullpath))
        with open(fullpath, "wb") as f:
            f.write(content)
        return os.path.realpath(fullpath)

    def write_wheel(self, filepath, content=b""):
        return self.write_file("wheels/" + filepath, content)
