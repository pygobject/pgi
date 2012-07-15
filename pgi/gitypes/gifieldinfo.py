# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import Enum, gint, gboolean, gpointer
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from gitypeinfo import GITypeInfoPtr
from giargument import GIArgument
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_field_info(base_info, _type=GIInfoType.FIELD):
    return base_info.get_type().value == _type


class GIFieldInfoFlags(Enum):
    IS_READABLE = 1 << 0
    IS_WRITABLE = 1 << 1


class GIFieldInfo(GIBaseInfo):
    pass


class GIFieldInfoPtr(GIBaseInfoPtr):
    _type_ = GIFieldInfo

    def __repr__(self):
        values = {}
        values["flags"] = self.get_flags()
        values["size"] = self.get_size()
        values["offset"] = self.get_offset()
        values["type"] = self.get_type()
        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)


_methods = [
    ("get_flags", GIFieldInfoFlags, [GIFieldInfoPtr]),
    ("get_size", gint, [GIFieldInfoPtr]),
    ("get_offset", gint, [GIFieldInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIFieldInfoPtr]),
    ("get_field", gboolean, [GIFieldInfoPtr, gpointer, POINTER(GIArgument)]),
    ("set_field", gboolean, [GIFieldInfoPtr, gpointer, POINTER(GIArgument)]),
]

wrap_class(_gir, GIFieldInfo, GIFieldInfoPtr, "g_field_info_", _methods)

__all__ = ["GIFieldInfo", "GIFieldInfoPtr", "GIFieldInfoFlags",
           "gi_is_field_info"]
