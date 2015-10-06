from __future__ import absolute_import, print_function

import os
import os.path

from landinggear.httpcache import HTTPCacheExtractor
from landinggear.wheelcache import WheelCacheExtractor


class Extractor(object):
    def __init__(self, package_dir, pip_cache_dir=None, symlink=True,
                 verbosity=1):
        self.pip_cache_dir = pip_cache_dir
        self.package_dir = package_dir
        assert package_dir is not None
        self.symlink = symlink
        self.verbosity = verbosity

        self.caches = [
            HTTPCacheExtractor(self.pip_cache_dir),
            WheelCacheExtractor(self.pip_cache_dir),
        ]

    def emit(self, msg, verbosity=1):
        if verbosity <= self.verbosity:
            print(msg)

    def iter_caches(self):
        for cache in self.caches:
            for cached_package in cache.iter_cache():
                yield cached_package

    def link_or_copy(self, cached_package):
        assert cached_package.is_package
        package_filepath = os.path.join(
            self.package_dir, cached_package.package_filename)
        if os.path.lexists(package_filepath):
            self.emit("Skipping already-extracted package: %s" % (
                cached_package.package_filename,), 2)
            return False
        if self.symlink and cached_package.can_symlink:
            self.emit("Creating symlink for package: %s" % (
                cached_package.package_filename,), 1)
            os.symlink(cached_package.filepath, package_filepath)
            return True
        with open(package_filepath, "wb") as f:
            self.emit("Extracting data for package: %s" % (
                cached_package.package_filename,), 1)
            f.write(cached_package.get_package_data())
        return True

    def extract_packages(self):
        objects = 0
        packages = 0
        extracted = 0
        if not os.path.exists(self.package_dir):
            self.emit("Creating package dir: %s" % (self.package_dir,))
            os.mkdir(self.package_dir)
        for cached_package in self.iter_caches():
            objects += 1
            if cached_package.is_package:
                packages += 1
                if self.link_or_copy(cached_package):
                    extracted += 1
        self.emit("%s (out of %s) cached packages extracted to: %s" % (
            extracted, packages, self.package_dir), 0)
        return objects, packages, extracted
