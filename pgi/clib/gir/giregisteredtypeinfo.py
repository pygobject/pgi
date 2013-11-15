# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ..glib import gchar_p
from ..gobject import GType
from .gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_registered_type_info(base_info, _it=GIInfoType):
    type_ = base_info.type.value
    return type_ in (_it.BOXED, _it.ENUM, _it.FLAGS, _it.INTERFACE, _it.OBJECT,
                     _it.STRUCT, _it.UNION)


class GIRegisteredTypeInfo(GIBaseInfo):
    pass


class GIRegisteredTypeInfoPtr(GIBaseInfoPtr):
    _type_ = GIRegisteredTypeInfo

    def _get_repr(self):
        values = super(GIRegisteredTypeInfoPtr, self)._get_repr()
        values["type_name"] = repr(self.type_name)
        values["type_init"] = repr(self.type_init)
        values["g_type"] = repr(self.g_type)
        return values

_methods = [
    ("get_type_name", gchar_p, [GIRegisteredTypeInfoPtr]),
    ("get_type_init", gchar_p, [GIRegisteredTypeInfoPtr]),
    ("get_g_type", GType, [GIRegisteredTypeInfoPtr]),
]

wrap_class(_gir, GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr,
           "g_registered_type_info_", _methods)

__all__ = ["GIRegisteredTypeInfo", "GIRegisteredTypeInfoPtr",
           "gi_is_registered_type_info"]
