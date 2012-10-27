# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from glib import gint64, gint
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from gicallableinfo import GIFunctionInfoPtr
from gitypeinfo import GITypeTag
from giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_value_info(base_info, _type=GIInfoType.VALUE):
    return base_info.get_type().value == _type


class GIValueInfo(GIBaseInfo):
    pass


class GIValueInfoPtr(GIBaseInfoPtr):
    _type_ = GIValueInfo

    def __repr__(self):
        values = {}
        values["value"] = self.get_value()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))

        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_value", gint64, [GIValueInfoPtr]),
]

wrap_class(_gir, GIValueInfo, GIValueInfoPtr, "g_value_info_", _methods)


def gi_is_enum_info(base_info):
    it = GIInfoType
    return base_info.get_type().value in (it.ENUM, it.FLAGS)


class GIEnumInfo(GIRegisteredTypeInfo):
    pass


class GIEnumInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIEnumInfo

    def __repr__(self):
        values = {}
        values["n_values"] = self.get_n_values()
        values["n_methods"] = self.get_n_methods()
        values["storage_type"] = self.get_storage_type()
        args = map(self.get_value, xrange(self.get_n_values()))
        values["values"] = args
        args = map(self.get_method, xrange(self.get_n_methods()))
        values["methods"] = args

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))

        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_n_values", gint, [GIEnumInfoPtr]),
    ("get_value", GIValueInfoPtr, [GIEnumInfoPtr, gint]),
    ("get_n_methods", gint, [GIEnumInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIEnumInfoPtr]),
    ("get_storage_type", GITypeTag, [GIEnumInfoPtr]),
]

wrap_class(_gir, GIEnumInfo, GIEnumInfoPtr, "g_enum_info_", _methods)

__all__ = ["GIEnumInfo", "GIEnumInfoPtr", "gi_is_enum_info",
           "GIValueInfo", "GIValueInfoPtr", "gi_is_value_info"]
