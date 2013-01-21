# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER

from pgi.glib import Flags, gint, gboolean, gpointer
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from gitypeinfo import GITypeInfoPtr
from giargument import GIArgument
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_field_info(base_info, _type=GIInfoType.FIELD):
    return base_info.type.value == _type


class GIFieldInfoFlags(Flags):
    IS_READABLE = 1 << 0
    IS_WRITABLE = 1 << 1


class GIFieldInfo(GIBaseInfo):
    pass


class GIFieldInfoPtr(GIBaseInfoPtr):
    _type_ = GIFieldInfo

    def _get_repr(self):
        values = super(GIFieldInfoPtr, self)._get_repr()
        values["flags"] = repr(self.flags)
        values["size"] = repr(self.size)
        values["offset"] = repr(self.offset)
        type_ = self.get_type()
        values["type"] = repr(type_)
        type_.unref()
        return values

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
