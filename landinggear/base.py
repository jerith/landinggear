from __future__ import absolute_import, print_function

import os.path

from pip.locations import USER_CACHE_DIR
from pip.utils import normalize_path


class LandingGearError(Exception):
    pass


def pip_cache_subdir(subdir, pip_cache_dir=None):
    if pip_cache_dir is None:
        pip_cache_dir = USER_CACHE_DIR
    return normalize_path(os.path.join(pip_cache_dir, subdir))


class CacheExtractor(object):
    """
    Extracts packages from pip's cache.
    """

    def __init__(self, pip_cache_dir=None):
        raise NotImplementedError()

    def iter_cache(self):
        raise NotImplementedError()


class CachedPackage(object):
    """
    A potential cached package.
    """

    can_symlink = False

    @property
    def is_package(self):
        if not hasattr(self, "_is_package"):
            self._is_package = self.check_package()
        return self._is_package

    @property
    def package_filename(self):
        if not hasattr(self, "_package_filename"):
            self._package_filename = self.get_package_filename()
        return self._package_filename

    def get_package_data(self):
        raise NotImplementedError()

    def check_package(self):
        return self.package_filename is not None

    def get_package_filename(self):
        raise NotImplementedError()
