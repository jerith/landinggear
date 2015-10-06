from __future__ import print_function, absolute_import

import os
import os.path
from zipfile import ZipFile, BadZipfile
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO  # noqa

from pip.download import SafeFileCache, CacheControlAdapter
from wheel.pkginfo import read_pkg_info_bytes

from landinggear.base import pip_cache_subdir, CacheExtractor, CachedPackage


class HTTPCacheExtractor(CacheExtractor):
    """
    Extracts wheels from the HTTP cache.

    TODO: Support non-wheels?
    """

    def __init__(self, pip_cache_dir=None):
        self.http_cache_dir = pip_cache_subdir("http", pip_cache_dir)
        self.adapter = CacheControlAdapter(SafeFileCache(self.http_cache_dir))
        self.serializer = self.adapter.controller.serializer

    def iter_cache(self):
        for root, dirs, files in os.walk(self.adapter.cache.directory):
            for file in files:
                yield CachedResponse(os.path.join(root, file), self.serializer)


class CachedResponse(CachedPackage):
    def __init__(self, filepath, serializer):
        self.filepath = filepath
        self.serializer = serializer
        self.resp_data = self.get_resp_data()

    def get_package_filename(self):
        return self.get_wheel_filename()

    def get_package_data(self):
        return self.get_resp_data()

    def get_resp_data(self):
        with open(self.filepath, "rb") as f:
            cached_data = f.read()
        resp = self.serializer.loads(
            FakeRequest(), cached_data)
        if resp is not None:
            return resp.read(decode_content=True)
        return None

    def get_wheel_filename(self):
        try:
            zipfile = ZipFile(BytesIO(self.resp_data))
        except BadZipfile:
            # The response was not a zipfile and therefore not a wheel.
            return None
        for zipinfo in zipfile.infolist():
            dirname, filename = os.path.split(zipinfo.filename)
            if filename == "WHEEL" and dirname.endswith(".dist-info"):
                if os.path.dirname(dirname):
                    # This isn't a top-level dir, so we don't want it.
                    continue
                return "%s-%s.whl" % (
                    dirname[:-len(".dist-info")],
                    self._collect_tags(zipfile.read(zipinfo)))

    def _collect_tags(self, wheel_metadata):
        pyver, abi, plat = set(), set(), set()
        pkginfo = read_pkg_info_bytes(wheel_metadata)
        tags = pkginfo.get_all("tag")
        for tag in tags:
            t_pyver, t_abi, t_plat = tag.split("-")
            pyver.add(t_pyver)
            abi.add(t_abi)
            plat.add(t_plat)
        return "%s-%s-%s" % tuple([
            ".".join(sorted(tag)) for tag in (pyver, abi, plat)])


class FakeRequest(object):
    def __init__(self, headers=None):
        self.headers = headers
        if self.headers is None:
            self.headers = {"Accept-Encoding": "gzip, deflate"}
