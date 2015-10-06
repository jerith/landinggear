from __future__ import print_function, absolute_import

import os
import os.path

from landinggear.base import pip_cache_subdir, CacheExtractor, CachedPackage


class WheelCacheExtractor(CacheExtractor):
    """
    Extracts wheels from the wheel cache.
    """

    def __init__(self, pip_cache_dir=None):
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
