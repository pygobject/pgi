# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import *
from glib import *
from gitypelib import *

from _util import wrap_class, load

_gir = load("girepository-1.0")


class GIInfoType(Enum):
    (INVALID, FUNCTION, CALLBACK, STRUCT, BOXED, ENUM, FLAGS, OBJECT,
     INTERFACE, CONSTANT, INVALID_0, UNION, VALUE, SIGNAL, VFUNC, PROPERTY,
     FIELD, ARG, TYPE, UNRESOLVED) = range(20)

_methods = [
    ("to_string", gchar_p, [GIInfoType]),
]

wrap_class(_gir, GIInfoType, None, "g_info_type_", _methods)


class GIAttributeIter(Structure):
    _fields_ = [
        ("data", gpointer),
        ("data2", gpointer),
        ("data3", gpointer),
        ("data4", gpointer),
    ]


class GIBaseInfo(Structure):
    _fields_ = [
        ("dummy1", gint32),
        ("dummy2", gint32),
        ("dummy3", gpointer),
        ("dummy4", gpointer),
        ("dummy5", gpointer),
        ("dummy6", guint32),
        ("dummy7", guint32),
        ("padding", gpointer * 4),
    ]


class GIBaseInfoPtr(POINTER(GIBaseInfo)):
    _type_ = GIBaseInfo

    def __repr__(self):
        values = {}
        values["type"] = self.get_type()
        values["name"] = self.get_name()
        values["namespace"] = self.get_namespace()
        values["deprecated"] = self.is_deprecated()
        container = self.get_container()
        if container:
            values["container"] = container
        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("ref", GIBaseInfoPtr, [GIBaseInfoPtr]),
    ("unref", None, [GIBaseInfoPtr]),
    ("get_type", GIInfoType, [GIBaseInfoPtr]),
    ("get_name", gchar_p, [GIBaseInfoPtr]),
    ("get_namespace", gchar_p, [GIBaseInfoPtr]),
    ("is_deprecated", gboolean, [GIBaseInfoPtr]),
    ("get_attribute", gchar_p, [GIBaseInfoPtr, gchar_p]),
    ("iterate_attributes", gboolean, [GIBaseInfoPtr, POINTER(GIAttributeIter),
                                      POINTER(c_char_p), POINTER(c_char_p)]),
    ("get_container", GIBaseInfoPtr, [GIBaseInfoPtr]),
    ("get_typelib", GITypelibPtr, [GIBaseInfoPtr]),
    ("equal", gboolean, [GIBaseInfoPtr, GIBaseInfoPtr]),
]

wrap_class(_gir, GIBaseInfo, GIBaseInfoPtr, "g_base_info_", _methods)

__all__ = ["GIInfoType", "GIAttributeIter", "GIBaseInfo", "GIBaseInfoPtr"]
