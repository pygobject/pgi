# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gifieldinfo import *
from gicallableinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_struct_info(base_info):
    return base_info.get_type().value == GIInfoType.STRUCT


class GIStructInfo(GIBaseInfo):
    pass


class GIStructInfoPtr(POINTER(GIStructInfo)):
    _type_ = GIStructInfo

_methods = [
    ("get_n_fields", gint, [GIStructInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIStructInfoPtr, gint]),
    ("get_n_methods", gint, [GIStructInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIStructInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIStructInfoPtr, gchar_p]),
    ("get_size", gsize, [GIStructInfoPtr]),
    ("get_alignment", gsize, [GIStructInfoPtr]),
    ("is_gtype_struct", gboolean, [GIStructInfoPtr]),
    ("is_foreign", gboolean, [GIStructInfoPtr]),
]

wrap_class(_gir, GIStructInfo, GIStructInfoPtr, "g_struct_info_", _methods)

__all__ = ["GIStructInfo", "GIStructInfoPtr", "gi_is_struct_info"]
