# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER

from ..glib import gint
from .gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from .gitypeinfo import GITypeInfoPtr
from .giargument import GIArgument
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_constant_info(base_info, _type=GIInfoType.CONSTANT):
    return base_info.type.value == _type


class GIConstantInfo(GIBaseInfo):
    pass


class GIConstantInfoPtr(GIBaseInfoPtr):
    _type_ = GIConstantInfo

    def _get_repr(self):
        values = super(GIConstantInfoPtr, self)._get_repr()
        values["type"] = repr(self.get_type())
        return values

_methods = [
    ("get_type", GITypeInfoPtr, [GIConstantInfoPtr], True),
    ("get_value", gint, [GIConstantInfoPtr, POINTER(GIArgument)]),
]

wrap_class(_gir, GIConstantInfo, GIConstantInfoPtr,
           "g_constant_info_", _methods)

__all__ = ["GIConstantInfo", "GIConstantInfoPtr", "gi_is_constant_info"]
