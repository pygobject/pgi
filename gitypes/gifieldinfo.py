# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gitypeinfo import *
from giargument import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_field_info(base_info):
    return base_info.get_type().value == GIInfoType.FIELD


class GIFieldInfoFlags(guint):
    IS_READABLE = 1 << 0
    IS_WRITABLE = 1 << 1


class GIFieldInfo(GIBaseInfo):
    pass


class GIFieldInfoPtr(POINTER(GIFieldInfo)):
    _type_ = GIFieldInfo

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
