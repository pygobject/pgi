# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gitypeinfo import *
from giargument import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_constant_info(base_info):
    return base_info.get_type().value == GIInfoType.CONSTANT


class GIConstantInfo(GIBaseInfo):
    pass


class GIConstantInfoPtr(POINTER(GIConstantInfo)):
    _type_ = GIConstantInfo

_methods = [
    ("get_type", GITypeInfoPtr, [GIConstantInfoPtr]),
    ("get_value", gint, [GIConstantInfoPtr, POINTER(GIArgument)]),
]

wrap_class(_gir, GIConstantInfo, GIConstantInfoPtr,
           "g_constant_info_", _methods)

__all__ = ["GIConstantInfo", "GIConstantInfoPtr", "gi_is_constant_info"]
