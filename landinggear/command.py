from __future__ import absolute_import, print_function

import sys
from optparse import OptionParser

from landinggear.extract_packages import Extractor


def parse_args(args):
    usage = "usage: %prog [options] PACKAGE_DIR"
    description = "".join([
        "Extract packages from the various pip caches to PACKAGE_DIR."
    ])
    parser = OptionParser(usage=usage, description=description)
    parser.set_defaults(pip_cache_dir=None, package_dir=None, symlink=True,
                        verbose=1, quiet=0)
    parser.add_option("--pip-cache-dir", dest="pip_cache_dir",
                      help="location of pip cache")
    parser.add_option("--symlink", dest="symlink", action="store_true",
                      help="create symlinks where possible")
    parser.add_option("--no-symlink", dest="symlink", action="store_false",
                      help="do not create symlinks")
    parser.add_option("-v", "--verbose", dest="verbose", action="count",
                      help="increase verbosity level")
    parser.add_option("-q", "--quiet", dest="quiet", action="count",
                      help="decrease verbosity level")

    (options, args) = parser.parse_args(args)

    if len(args) < 1:
        parser.error("no PACKAGE_DIR provided")
    elif len(args) > 1:
        parser.error("too many arguments")
    [options.package_dir] = args
    return options


def extract_packages(args):
    opts = parse_args(args)
    verbosity = opts.verbose - opts.quiet
    extractor = Extractor(
        opts.package_dir, opts.pip_cache_dir, opts.symlink, verbosity)
    extractor.extract_packages()


def main():
    extract_packages(sys.argv[1:])
