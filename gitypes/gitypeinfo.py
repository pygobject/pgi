# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER
from glib import *
from gibaseinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_type_info(base_info):
    return base_info.get_type().value == GIInfoType.TYPE


class GIArrayType(guint):
    C, ARRAY, PTR_ARRAY, BYTE_ARRAY = range(4)


class GITypeTag(guint):
    VOID = 0
    BOOLEAN = 1
    INT8 = 2
    UINT8 = 3
    INT16 = 4
    UINT16 = 5
    INT32 = 6
    UINT32 = 7
    INT64 = 8
    UINT64 = 9
    FLOAT = 10
    DOUBLE = 11
    GTYPE = 12
    UTF8 = 13
    FILENAME = 14
    ARRAY = 15
    INTERFACE = 16
    GLIST = 17
    GSLIST = 18
    GHASH = 19
    ERROR = 20
    UNICHAR = 21

    @classmethod
    def is_basic(cls, tag):
        return (tag < cls.ARRAY or tag == cls.UNICHAR)

_methods = [
    ("to_string", gchar_p, [GITypeTag]),
]

wrap_class(_gir, GITypeTag, None, "g_type_tag_", _methods)


class GITypeInfo(GIBaseInfo):
    pass


class GITypeInfoPtr(POINTER(GITypeInfo)):
    _type_ = GITypeInfo

_methods = [
    ("is_pointer", gboolean, [GITypeInfoPtr]),
    ("get_tag", GITypeTag, [GITypeInfoPtr]),
    ("get_param_type", GITypeInfoPtr, [GITypeInfoPtr]),
    ("get_interface", GIBaseInfoPtr, [GITypeInfoPtr]),
    ("get_array_length", gint, [GITypeInfoPtr]),
    ("get_array_fixed_size", gint, [GITypeInfoPtr]),
    ("is_zero_terminated", gboolean, [GITypeInfoPtr]),
    ("get_array_type", GIArrayType, [GITypeInfoPtr]),
]

wrap_class(_gir, GITypeInfo, GITypeInfoPtr, "g_type_info_", _methods)

__all__ = ["GIArrayType", "GITypeTag", "GITypeInfo", "GITypeInfoPtr",
           "gi_is_type_info"]
