landinggear
===========

``landinggear`` was born out of the complaints of some friends who travel a lot
and like to write software while on aeroplanes. Its purpose is to liberate
wheels from the depths of the ``pip`` cache so they can be installed without an
internet connection (while flying over the middle of the Atlantic, for
example).

usage
-----

Use ``landinggear path/to/wheelhouse`` to populate your wheelhouse from your
pip cache. Then use ``pip install --no-index -f path/to/wheelhouse mypackage``
to install packages.

how it works
------------

Since version 7.0, ``pip`` always installs packages from wheels, building them
from source packages if necessary. All downloads are cached in the HTTP cache
and any wheels pip builds itself are cached in the wheel cache. ``landinggear``
looks for wheels in both of these caches.

The wheel cache is a directory tree containing wheel files inside source-hash
named directories. These are liberated by walking the tree to find them and
then symlinking (or copying) them.

The HTTP cache is also a directory tree, but it contains serialized HTTP
responses with opaque names. ``landinggear`` deserializes and inspects these,
looking for zipfiles containing wheel metadata. Liberation involves extracting
the deserialized HTTP response into a new file with the filename carefully
reconstructed from the metadata.

caveats
-------

``pip`` doesn't really have a stable internal API, so it's possible that some
of the trickery ``landinggear`` relies on will stop working with the next
release. I've tried to stick to major things that are unlikely to change,
however.

TODO
----

Figure out how to write some more useful tests.
