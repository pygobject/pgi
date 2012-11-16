# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi.glib import gint, gchar_p, gsize, gboolean
from gibaseinfo import GIInfoType
from gifieldinfo import GIFieldInfoPtr
from gicallableinfo import GIFunctionInfoPtr
from giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_struct_info(base_info, _type=GIInfoType.STRUCT):
    return base_info.get_type().value == _type


class GIStructInfo(GIRegisteredTypeInfo):
    pass


class GIStructInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIStructInfo

    def __repr__(self):
        values = {}
        values["size"] = self.get_size()
        values["alignment"] = self.get_alignment()
        values["is_gtype_struct"] = self.is_gtype_struct()
        values["is_foreign"] = self.is_foreign()
        values["methods"] = self.get_n_methods()
        values["fields"] = self.get_n_fields()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_n_fields", gint, [GIStructInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIStructInfoPtr, gint]),
    ("get_n_methods", gint, [GIStructInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIStructInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIStructInfoPtr, gchar_p]),
    ("get_size", gsize, [GIStructInfoPtr]),
    ("get_alignment", gsize, [GIStructInfoPtr]),
    ("is_gtype_struct", gboolean, [GIStructInfoPtr]),
    ("is_foreign", gboolean, [GIStructInfoPtr]),
]

wrap_class(_gir, GIStructInfo, GIStructInfoPtr, "g_struct_info_", _methods)

__all__ = ["GIStructInfo", "GIStructInfoPtr", "gi_is_struct_info"]
