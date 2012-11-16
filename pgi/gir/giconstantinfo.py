# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from pgi.glib import gint
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from gitypeinfo import GITypeInfoPtr
from giargument import GIArgument
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_constant_info(base_info, _type=GIInfoType.CONSTANT):
    return base_info.get_type().value == _type


class GIConstantInfo(GIBaseInfo):
    pass


class GIConstantInfoPtr(GIBaseInfoPtr):
    _type_ = GIConstantInfo

_methods = [
    ("get_type", GITypeInfoPtr, [GIConstantInfoPtr]),
    ("get_value", gint, [GIConstantInfoPtr, POINTER(GIArgument)]),
]

wrap_class(_gir, GIConstantInfo, GIConstantInfoPtr,
           "g_constant_info_", _methods)

__all__ = ["GIConstantInfo", "GIConstantInfoPtr", "gi_is_constant_info"]
