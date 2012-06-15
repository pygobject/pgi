# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from gobject import *
from gibaseinfo import *
from gitypeinfo import *
from giarginfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_property_info(base_info):
    return base_info.get_type().value == GIInfoType.PROPERTY


class GIPropertyInfo(GIBaseInfo):
    pass


class GIPropertyInfoPtr(POINTER(GIPropertyInfo)):
    _type_ = GIPropertyInfo

_methods = [
    ("get_flags", GParamFlags, [GIPropertyInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIPropertyInfoPtr]),
    ("get_ownership_transfer", GITransfer, [GIPropertyInfoPtr]),
]

wrap_class(_gir, GIPropertyInfo, GIPropertyInfoPtr,
           "g_property_info_", _methods)

__all__ = ["GIPropertyInfo", "GIPropertyInfoPtr", "gi_is_property_info"]
