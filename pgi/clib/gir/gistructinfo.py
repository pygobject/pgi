# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ..glib import gint, gchar_p, gsize, gboolean
from .gibaseinfo import GIInfoType, GIBaseInfo
from .gifieldinfo import GIFieldInfo
from .gicallableinfo import GIFunctionInfo
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


@GIBaseInfo._register(GIInfoType.STRUCT)
class GIStructInfo(GIRegisteredTypeInfo):

    def _get_repr(self):
        values = super(GIStructInfo, self)._get_repr()
        values = {}
        values["size"] = repr(self.size)
        values["alignment"] = repr(self.alignment)
        values["is_gtype_struct"] = repr(self.is_gtype_struct)
        values["is_foreign"] = repr(self.is_foreign)
        values["methods"] = repr(self.get_methods())
        values["fields"] = repr(self.get_fields())
        return values

    def get_fields(self):
        return map(self.get_field, xrange(self.n_fields))

    def get_methods(self):
        return map(self.get_method, xrange(self.n_methods))

_methods = [
    ("get_n_fields", gint, [GIStructInfo]),
    ("get_field", GIFieldInfo, [GIStructInfo, gint], True),
    ("get_n_methods", gint, [GIStructInfo]),
    ("get_method", GIFunctionInfo, [GIStructInfo, gint], True),
    ("find_method", GIFunctionInfo, [GIStructInfo, gchar_p], True),
    ("get_size", gsize, [GIStructInfo]),
    ("get_alignment", gsize, [GIStructInfo]),
    ("is_gtype_struct", gboolean, [GIStructInfo]),
    ("is_foreign", gboolean, [GIStructInfo]),
]

wrap_class(_gir, GIStructInfo, GIStructInfo, "g_struct_info_", _methods)

__all__ = ["GIStructInfo"]
