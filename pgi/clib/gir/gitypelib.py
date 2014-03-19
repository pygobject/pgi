# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER, c_void_p

from ..glib import guint8, gsize, gboolean, gchar_p, gpointer
from ..glib import GError, GMappedFilePtr
from .._utils import wrap_class, find_library


_gir = find_library("girepository-1.0")


class GITypelib(c_void_p):

    def __repr__(self):
        values = {}
        values["namespace"] = self.namespace
        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (type(self).__name__, l)

_methods = [
    ("new_from_memory",
        GITypelib, [POINTER(guint8), gsize, POINTER(POINTER(GError))]),
    ("new_from_const_memory",
        GITypelib, [POINTER(guint8), gsize, POINTER(POINTER(GError))]),
    ("new_from_mapped_file",
        GITypelib, [GMappedFilePtr, POINTER(POINTER(GError))]),
    ("free", None, [GITypelib]),
    ("symbol", gboolean, [GITypelib, gchar_p, POINTER(gpointer)]),
    ("get_namespace", gchar_p, [GITypelib]),
]

wrap_class(_gir, GITypelib, GITypelib, "g_typelib_", _methods)

__all__ = ["GITypelib"]
