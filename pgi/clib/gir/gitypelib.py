# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER, Structure

from ..glib import guint8, gsize, gboolean, gchar_p, gpointer
from ..glib import GError, GMappedFilePtr
from ..ctypesutil import wrap_class, find_library

_gir = find_library("girepository-1.0")


class GITypelib(Structure):
    pass


class GITypelibPtr(POINTER(GITypelib)):
    _type_ = GITypelib

    def __repr__(self):
        values = {}
        values["namespace"] = self.namespace
        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("new_from_memory",
        GITypelibPtr, [POINTER(guint8), gsize, POINTER(POINTER(GError))]),
    ("new_from_const_memory",
        GITypelibPtr, [POINTER(guint8), gsize, POINTER(POINTER(GError))]),
    ("new_from_mapped_file",
        GITypelibPtr, [GMappedFilePtr, POINTER(POINTER(GError))]),
    ("free", None, [GITypelibPtr]),
    ("symbol", gboolean, [GITypelibPtr, gchar_p, POINTER(gpointer)]),
    ("get_namespace", gchar_p, [GITypelibPtr]),
]

wrap_class(_gir, GITypelib, GITypelibPtr, "g_typelib_", _methods)

__all__ = ["GITypelib", "GITypelibPtr"]
