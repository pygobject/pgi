# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ..glib import gint, gchar_p
from .gibaseinfo import GIInfoType, GIBaseInfoPtr
from .gipropertyinfo import GIPropertyInfoPtr
from .gicallableinfo import GIFunctionInfoPtr, GISignalInfoPtr, GIVFuncInfoPtr
from .giconstantinfo import GIConstantInfoPtr
from .gistructinfo import GIStructInfoPtr
from .giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_interface_info(base_info, _type=GIInfoType.INTERFACE):
    return base_info.type.value == _type


class GIInterfaceInfo(GIRegisteredTypeInfo):
    pass


class GIInterfaceInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIInterfaceInfo

    def get_methods(self):
        return map(self.get_method, xrange(self.n_methods))

    def get_properties(self):
        return map(self.get_property, xrange(self.n_properties))

    def get_signals(self):
        return map(self.get_signal, xrange(self.n_signals))

    def get_constants(self):
        return map(self.get_constant, xrange(self.n_constants))

    def get_prerequisites(self):
        return map(self.get_prerequisite, xrange(self.n_prerequisites))

    def _get_repr(self):
        values = super(GIInterfaceInfoPtr, self)._get_repr()
        values["n_constants"] = repr(self.n_constants)
        values["n_signals"] = repr(self.n_signals)
        values["n_methods"] = repr(self.n_methods)
        values["n_properties"] = repr(self.n_properties)
        values["n_prerequisites"] = repr(self.n_prerequisites)
        return values

_methods = [
    ("get_n_prerequisites", gint, [GIInterfaceInfoPtr]),
    ("get_prerequisite", GIBaseInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("get_n_properties", gint, [GIInterfaceInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("get_n_methods", gint, [GIInterfaceInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("find_method", GIFunctionInfoPtr, [GIInterfaceInfoPtr, gchar_p], True),
    ("get_n_signals", gint, [GIInterfaceInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("get_n_vfuncs", gint, [GIInterfaceInfoPtr]),
    ("get_vfunc", GIVFuncInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("get_n_constants", gint, [GIInterfaceInfoPtr]),
    ("get_constant", GIConstantInfoPtr, [GIInterfaceInfoPtr, gint], True),
    ("get_iface_struct", GIStructInfoPtr, [GIInterfaceInfoPtr], True),
    ("find_vfunc", GIVFuncInfoPtr, [GIInterfaceInfoPtr, gchar_p], True),
]

wrap_class(_gir, GIInterfaceInfo, GIInterfaceInfoPtr,
           "g_interface_info_", _methods)

__all__ = ["GIInterfaceInfo", "GIInterfaceInfoPtr", "gi_is_interface_info"]
