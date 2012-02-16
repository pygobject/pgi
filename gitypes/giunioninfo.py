# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gifieldinfo import *
from gicallableinfo import *
from gitypeinfo import *
from giconstantinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_union_info(base_info):
    return base_info.get_type().value == GIInfoType.UNION


class GIUnionInfo(GIBaseInfo):
    pass


class GIUnionInfoPtr(POINTER(GIUnionInfo)):
    _type_ = GIUnionInfo

_methods = [
    ("get_n_fields", gint, [GIUnionInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIUnionInfoPtr, gint]),
    ("get_n_methods", gint, [GIUnionInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gint]),
    ("is_discriminated", gboolean, [GIUnionInfoPtr]),
    ("get_discriminator_offset", gint, [GIUnionInfoPtr]),
    ("get_discriminator_type", GITypeInfoPtr, [GIUnionInfoPtr]),
    ("get_discriminator", GIConstantInfoPtr, [GIUnionInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gchar_p]),
    ("get_size", gsize, [GIUnionInfoPtr]),
    ("get_alignment", gsize, [GIUnionInfoPtr]),
]

wrap_class(_gir, GIUnionInfo, GIUnionInfoPtr, "g_union_info_", _methods)

__all__ = ["GIUnionInfo", "GIUnionInfoPtr", "gi_is_union_info"]
