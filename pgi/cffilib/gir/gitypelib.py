# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ._ffi import ffi, lib


class GITypelib(object):
    def __init__(self, ptr):
        self._ptr = ptr

    def free(self):
        lib.g_typelib_free(self._ptr)

    @property
    def namespace(self):
        return ffi.string(lib.g_typelib_get_namespace(self._ptr))

    def __repr__(self):
        return "<%s namespace=%r>" % (type(self).__name__, self.namespace)
