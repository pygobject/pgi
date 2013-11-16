# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ..glib import gint64, gint
from .gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from .gicallableinfo import GIFunctionInfoPtr
from .gitypeinfo import GITypeTag
from .giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_value_info(base_info, _type=GIInfoType.VALUE):
    return base_info.type.value == _type


class GIValueInfo(GIBaseInfo):
    pass


class GIValueInfoPtr(GIBaseInfoPtr):
    _type_ = GIValueInfo

    def _get_repr(self):
        values = super(GIValueInfoPtr, self)._get_repr()
        values["value"] = repr(self.value)
        return values

_methods = [
    ("get_value", gint64, [GIValueInfoPtr]),
]

wrap_class(_gir, GIValueInfo, GIValueInfoPtr, "g_value_info_", _methods)


def gi_is_enum_info(base_info):
    return base_info.type.value in (GIInfoType.ENUM, GIInfoType.FLAGS)


class GIEnumInfo(GIRegisteredTypeInfo):
    pass


class GIEnumInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIEnumInfo

    def get_values(self):
        return map(self.get_value, xrange(self.n_values))

    def get_methods(self):
        return map(self.get_method, xrange(self.n_methods))

    def _get_repr(self):
        values = super(GIEnumInfoPtr, self)._get_repr()
        values["n_values"] = repr(self.n_values)
        values["n_methods"] = repr(self.n_methods)
        values["storage_type"] = repr(self.storage_type)
        return values

_methods = [
    ("get_n_values", gint, [GIEnumInfoPtr]),
    ("get_value", GIValueInfoPtr, [GIEnumInfoPtr, gint], True),
    ("get_n_methods", gint, [GIEnumInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIEnumInfoPtr], True),
    ("get_storage_type", GITypeTag, [GIEnumInfoPtr]),
]

wrap_class(_gir, GIEnumInfo, GIEnumInfoPtr, "g_enum_info_", _methods)

__all__ = ["GIEnumInfo", "GIEnumInfoPtr", "gi_is_enum_info",
           "GIValueInfo", "GIValueInfoPtr", "gi_is_value_info"]
