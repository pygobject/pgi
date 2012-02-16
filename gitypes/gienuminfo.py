# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gicallableinfo import *
from gitypeinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")

# GIValueInfo


def gi_is_value_info(base_info):
    return base_info.get_type().value == GIInfoType.VALUE


class GIValueInfo(GIBaseInfo):
    pass


class GIValueInfoPtr(POINTER(GIValueInfo)):
    _type_ = GIValueInfo

_methods = [
    ("get_value", gint64, [GIValueInfoPtr]),
]

wrap_class(_gir, GIValueInfo, GIValueInfoPtr, "g_value_info_", _methods)

# GIEnumInfo


def gi_is_enum_info(base_info):
    it = GIInfoType
    return base_info.get_type().value in (it.ENUM, it.FLAGS)


class GIEnumInfo(GIBaseInfo):
    pass


class GIEnumInfoPtr(POINTER(GIEnumInfo)):
    _type_ = GIEnumInfo

_methods = [
    ("get_n_values", gint, [GIEnumInfoPtr]),
    ("get_value", GIValueInfoPtr, [GIEnumInfoPtr]),
    ("get_n_methods", gint, [GIEnumInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIEnumInfoPtr]),
    ("get_storage_type", GITypeTag, [GIEnumInfoPtr]),
]

wrap_class(_gir, GIEnumInfo, GIEnumInfoPtr, "g_enum_info_", _methods)

__all__ = ["GIEnumInfo", "GIEnumInfoPtr", "gi_is_enum_info",
           "GIValueInfo", "GIValueInfoPtr", "gi_is_value_info"]
