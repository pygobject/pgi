# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ..glib import gint, gchar_p
from .gibaseinfo import GIInfoType, GIBaseInfo
from .gipropertyinfo import GIPropertyInfo
from .gicallableinfo import GIFunctionInfo, GISignalInfo, GIVFuncInfo
from .giconstantinfo import GIConstantInfo
from .gistructinfo import GIStructInfo
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


@GIBaseInfo._register(GIInfoType.INTERFACE)
class GIInterfaceInfo(GIRegisteredTypeInfo):

    def get_methods(self):
        return map(self.get_method, xrange(self.n_methods))

    def get_properties(self):
        return map(self.get_property, xrange(self.n_properties))

    def get_signals(self):
        return map(self.get_signal, xrange(self.n_signals))

    def get_constants(self):
        return map(self.get_constant, xrange(self.n_constants))

    def get_vfuncs(self):
        return map(self.get_vfunc, xrange(self.n_vfuncs))

    def get_prerequisites(self):
        return map(self.get_prerequisite, xrange(self.n_prerequisites))

    def _get_repr(self):
        values = super(GIInterfaceInfo, self)._get_repr()
        values["n_constants"] = repr(self.n_constants)
        values["n_signals"] = repr(self.n_signals)
        values["n_methods"] = repr(self.n_methods)
        values["n_properties"] = repr(self.n_properties)
        values["n_prerequisites"] = repr(self.n_prerequisites)
        return values

_methods = [
    ("get_n_prerequisites", gint, [GIInterfaceInfo]),
    ("get_prerequisite", GIBaseInfo, [GIInterfaceInfo, gint], True),
    ("get_n_properties", gint, [GIInterfaceInfo]),
    ("get_property", GIPropertyInfo, [GIInterfaceInfo, gint], True),
    ("get_n_methods", gint, [GIInterfaceInfo]),
    ("get_method", GIFunctionInfo, [GIInterfaceInfo, gint], True),
    ("find_method", GIFunctionInfo, [GIInterfaceInfo, gchar_p], True),
    ("get_n_signals", gint, [GIInterfaceInfo]),
    ("get_signal", GISignalInfo, [GIInterfaceInfo, gint], True),
    ("find_signal", GISignalInfo, [GIInterfaceInfo, gchar_p], True),
    ("get_n_vfuncs", gint, [GIInterfaceInfo]),
    ("get_vfunc", GIVFuncInfo, [GIInterfaceInfo, gint], True),
    ("get_n_constants", gint, [GIInterfaceInfo]),
    ("get_constant", GIConstantInfo, [GIInterfaceInfo, gint], True),
    ("get_iface_struct", GIStructInfo, [GIInterfaceInfo], True),
    ("find_vfunc", GIVFuncInfo, [GIInterfaceInfo, gchar_p], True),
]

wrap_class(_gir, GIInterfaceInfo, GIInterfaceInfo,
           "g_interface_info_", _methods)

__all__ = ["GIInterfaceInfo"]
