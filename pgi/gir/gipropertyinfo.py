# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi.gobject import GParamFlags
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr
from gitypeinfo import GITypeInfoPtr, GIInfoType
from giarginfo import GITransfer
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_property_info(base_info, _type=GIInfoType.PROPERTY):
    return base_info.get_type().value == _type


class GIPropertyInfo(GIBaseInfo):
    pass


class GIPropertyInfoPtr(GIBaseInfoPtr):
    _type_ = GIPropertyInfo

    def _get_repr(self):
        values = super(GIPropertyInfoPtr, self)._get_repr()
        values["flags"] = repr(self.get_flags())
        type_ = self.get_type()
        values["type"] = repr(type_)
        type_.unref()
        values["ownership_transfer"] = repr(self.get_ownership_transfer())
        return values

_methods = [
    ("get_flags", GParamFlags, [GIPropertyInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIPropertyInfoPtr]),
    ("get_ownership_transfer", GITransfer, [GIPropertyInfoPtr]),
]

wrap_class(_gir, GIPropertyInfo, GIPropertyInfoPtr,
           "g_property_info_", _methods)

__all__ = ["GIPropertyInfo", "GIPropertyInfoPtr", "gi_is_property_info"]
