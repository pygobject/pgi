# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ._ffi import ffi, lib
from .._compat import PY3


class GITypelib(object):
    def __init__(self, ptr):
        self._ptr = ptr

    def free(self):
        lib.g_typelib_free(self._ptr)

    @property
    def namespace(self):
        res = lib.g_typelib_get_namespace(self._ptr)
        if res:
            res = ffi.string(res)
            if PY3:
                res = res.decode("ascii")
        return res

    def __repr__(self):
        return "<%s namespace=%r>" % (type(self).__name__, self.namespace)
