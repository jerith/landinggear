from __future__ import absolute_import, print_function

import os.path
from unittest import TestCase

from pip.locations import USER_CACHE_DIR

from landinggear.base import LandingGearError
from landinggear.tests.helpers import tempcache, tempdir
from landinggear.wheelcache import WheelCacheExtractor


def writefile(basedir, filepath, content=None):
    fullpath = os.path.join(basedir, *filepath.split("/"))
    os.makedirs(os.path.dirname(fullpath))
    with open(fullpath, "wb") as f:
        if content is not None:
            f.write("")
    return os.path.realpath(fullpath)


class TestWheelCache(TestCase):

    def test_default_pip_cache(self):
        """
        If no pip cache is provided, the default is used.
        """
        extractor = WheelCacheExtractor()
        self.assertEqual(
            extractor.wheel_cache_dir, os.path.join(USER_CACHE_DIR, "wheels"))

    def test_missing_pip_cache(self):
        """
        A missing pip cache dir throws an error.
        """
        with tempdir() as basedir:
            pip_cache_dir = os.path.join(basedir, "pipcache")
            self.assertRaises(
                LandingGearError, WheelCacheExtractor, pip_cache_dir)

    def test_missing_wheel_cache(self):
        """
        A pip cache dir with no wheel cache returns no packages.
        """
        with tempdir() as basedir:
            pip_cache_dir = os.path.join(basedir, "pipcache")
            os.mkdir(pip_cache_dir)
            extractor = WheelCacheExtractor(pip_cache_dir)
            self.assertEqual(list(extractor.iter_cache()), [])

    def test_empty_wheel_cache(self):
        """
        A pip cache dir with an empty wheel cache returns no packages.
        """
        with tempcache() as pipcache:
            extractor = WheelCacheExtractor(pipcache.path)
            self.assertEqual(list(extractor.iter_cache()), [])

    def test_pip_cache_with_wheels(self):
        """
        A pip wheel cache with wheels in it returns some packages.
        """
        with tempcache() as pipcache:
            wheel1 = pipcache.write_wheel("ab/cd/ef/ghij/foo.whl")
            wheel2 = pipcache.write_wheel("12/34/56/7890/bar.whl")
            extractor = WheelCacheExtractor(pipcache.path)
            self.assertEqual(
                sorted([cw.filepath for cw in extractor.iter_cache()]),
                sorted([wheel1, wheel2]))

    def test_wheel_content(self):
        """
        Any file ending with .whl is assumed to be a valid wheel.
        """
        with tempcache() as pipcache:
            pipcache.write_wheel("ab/cd/ef/ghij/foo.whl", b"round")
            extractor = WheelCacheExtractor(pipcache.path)
            [cached_wheel] = extractor.iter_cache()
            self.assertEqual(cached_wheel.can_symlink, True)
            self.assertEqual(cached_wheel.is_package, True)
            self.assertEqual(cached_wheel.package_filename, "foo.whl")
            self.assertEqual(cached_wheel.get_package_data(), b"round")
