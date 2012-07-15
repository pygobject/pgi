# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from glib import Enum, gchar_p, gboolean, gint
from gibaseinfo import GIInfoType, GIBaseInfo, GIBaseInfoPtr
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_type_info(base_info, _type=GIInfoType.TYPE):
    return base_info.get_type().value == _type


class GIArrayType(Enum):
    C, ARRAY, PTR_ARRAY, BYTE_ARRAY = range(4)


class GITypeTag(Enum):
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


class GITypeInfoPtr(GIBaseInfoPtr):
    _type_ = GITypeInfo

    def __repr__(self):
        values = {}
        values["is_pointer"] = self.is_pointer()
        values["tag"] = self.get_tag()
        type_ = self.get_tag().value
        if type_ == GITypeTag.INTERFACE:
            values["interface"] = self.get_interface()
        if type_ == GITypeTag.ARRAY:
            values["array_length"] = self.get_array_length()
            values["array_fixed_size"] = self.get_array_fixed_size()
            values["zero_terminated"] = self.is_zero_terminated()
            values["array_type"] = self.get_array_type()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))

        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("is_pointer", gboolean, [GITypeInfoPtr]),
    ("get_tag", GITypeTag, [GITypeInfoPtr]),
    ("get_param_type", GITypeInfoPtr, [GITypeInfoPtr, gint]),
    ("get_interface", GIBaseInfoPtr, [GITypeInfoPtr]),
    ("get_array_length", gint, [GITypeInfoPtr]),
    ("get_array_fixed_size", gint, [GITypeInfoPtr]),
    ("is_zero_terminated", gboolean, [GITypeInfoPtr]),
    ("get_array_type", GIArrayType, [GITypeInfoPtr]),
]

wrap_class(_gir, GITypeInfo, GITypeInfoPtr, "g_type_info_", _methods)

__all__ = ["GIArrayType", "GITypeTag", "GITypeInfo", "GITypeInfoPtr",
           "gi_is_type_info"]
