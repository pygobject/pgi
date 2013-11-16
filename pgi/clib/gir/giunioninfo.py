# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ..glib import gint, gboolean, gchar_p, gsize
from .gibaseinfo import GIInfoType
from .gifieldinfo import GIFieldInfoPtr
from .gicallableinfo import GIFunctionInfoPtr
from .gitypeinfo import GITypeInfoPtr
from .giconstantinfo import GIConstantInfoPtr
from .giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_union_info(base_info):
    return base_info.type.value == GIInfoType.UNION


class GIUnionInfo(GIRegisteredTypeInfo):
    pass


class GIUnionInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIUnionInfo

    def get_methods(self):
        return map(self.get_method, xrange(self.n_methods))

    def get_fields(self):
        return map(self.get_field, xrange(self.n_fields))

    def _get_repr(self):
        values = super(GIUnionInfoPtr, self)._get_repr()
        values = {}
        values["n_fields"] = repr(self.n_fields)
        values["is_discriminated"] = repr(self.is_discriminated)
        values["discriminator_offset"] = repr(self.discriminator_offset)
        values["discriminator_type"] = repr(self.get_discriminator_type())
        values["size"] = repr(self.size)
        values["alignment"] = repr(self.alignment)
        values["n_methods"] = repr(self.n_methods)

        return values

_methods = [
    ("get_n_fields", gint, [GIUnionInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIUnionInfoPtr, gint], True),
    ("get_n_methods", gint, [GIUnionInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gint], True),
    ("is_discriminated", gboolean, [GIUnionInfoPtr]),
    ("get_discriminator_offset", gint, [GIUnionInfoPtr]),
    ("get_discriminator_type", GITypeInfoPtr, [GIUnionInfoPtr], True),
    ("get_discriminator", GIConstantInfoPtr, [GIUnionInfoPtr, gint], True),
    ("find_method", GIFunctionInfoPtr, [GIUnionInfoPtr, gchar_p], True),
    ("get_size", gsize, [GIUnionInfoPtr]),
    ("get_alignment", gsize, [GIUnionInfoPtr]),
]

wrap_class(_gir, GIUnionInfo, GIUnionInfoPtr, "g_union_info_", _methods)

__all__ = ["GIUnionInfo", "GIUnionInfoPtr", "gi_is_union_info"]
