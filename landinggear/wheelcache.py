from __future__ import absolute_import, print_function

import os
import os.path

from landinggear.base import (
    CachedPackage, CacheExtractor, LandingGearError, pip_cache_subdir)


class WheelCacheExtractor(CacheExtractor):
    """
    Extracts wheels from the wheel cache.
    """

    def __init__(self, pip_cache_dir=None):
        if pip_cache_dir is not None and not os.path.isdir(pip_cache_dir):
            raise LandingGearError("Missing pip cache: %s" % (pip_cache_dir,))
        self.wheel_cache_dir = pip_cache_subdir("wheels", pip_cache_dir)

    def iter_cache(self):
        for root, dirs, files in os.walk(self.wheel_cache_dir):
            for file in files:
                yield CachedWheel(os.path.join(root, file))


class CachedWheel(CachedPackage):

    can_symlink = True

    def __init__(self, filepath):
        self.filepath = filepath

    def get_package_filename(self):
        if not self.filepath.endswith(".whl"):
            return None
        return os.path.basename(self.filepath)

    def get_package_data(self):
        with open(self.filepath, "rb") as f:
            return f.read()
