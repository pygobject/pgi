# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import c_char_p, CFUNCTYPE, c_void_p

from pgi.glib import gchar_p, gboolean, gint
from pgi.gobject import GValuePtr
from gibaseinfo import GIInfoType
from giinterfaceinfo import GIInterfaceInfoPtr
from gifieldinfo import GIFieldInfoPtr
from gipropertyinfo import GIPropertyInfoPtr
from gicallableinfo import GIFunctionInfoPtr, GISignalInfoPtr, GIVFuncInfoPtr
from giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from giconstantinfo import GIConstantInfoPtr
from gistructinfo import GIStructInfoPtr
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_object_info(base_info, _type=GIInfoType.OBJECT):
    return base_info.get_type().value == _type


class GIObjectInfo(GIRegisteredTypeInfo):
    pass


class GIObjectInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIObjectInfo

    def __repr__(self):
        values = {}
        values["type_name"] = self.get_type_name()
        values["type_init"] = self.get_type_init()
        values["abstract"] = self.get_abstract()
        values["fundamental"] = self.get_fundamental()
        #values["parent"] = self.get_parent()
        values["n_interfaces"] = self.get_n_interfaces()
        values["n_fields"] = self.get_n_fields()
        values["n_properties"] = self.get_n_properties()

        values["n_methods"] = self.get_n_methods()
        values["n_signals"] = self.get_n_signals()
        values["n_vfuncs"] = self.get_n_vfuncs()
        values["class_struct"] = self.get_class_struct()
        values["unref_function"] = self.get_unref_function()
        values["ref_function"] = self.get_ref_function()

        values["set_value_function"] = self.get_set_value_function()
        values["get_value_function"] = self.get_get_value_function()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

GIObjectInfoGetValueFunction = CFUNCTYPE(c_void_p, GValuePtr)
GIObjectInfoRefFunction = CFUNCTYPE(c_void_p, c_void_p)
GIObjectInfoSetValueFunction = CFUNCTYPE(None, GValuePtr, c_void_p)
GIObjectInfoUnrefFunction = CFUNCTYPE(None, c_void_p)

_methods = [
    ("get_type_name", gchar_p, [GIObjectInfoPtr]),
    ("get_type_init", gchar_p, [GIObjectInfoPtr]),
    ("get_abstract", gboolean, [GIObjectInfoPtr]),
    ("get_fundamental", gboolean, [GIObjectInfoPtr]),
    ("get_parent", GIObjectInfoPtr, [GIObjectInfoPtr]),
    ("get_n_interfaces", gint, [GIObjectInfoPtr]),
    ("get_interface", GIInterfaceInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_fields", gint, [GIObjectInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_properties", gint, [GIObjectInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_methods", gint, [GIObjectInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIObjectInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIObjectInfoPtr, gchar_p]),
    ("get_n_signals", gint, [GIObjectInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_vfuncs", gint, [GIObjectInfoPtr]),
    ("get_vfunc", GIVFuncInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_constants", gint, [GIObjectInfoPtr]),
    ("get_constant", GIConstantInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_class_struct", GIStructInfoPtr, [GIObjectInfoPtr]),
    ("find_vfunc", GIVFuncInfoPtr, [GIObjectInfoPtr, gchar_p]),
    ("get_unref_function", c_char_p, [GIObjectInfoPtr]),
    ("get_unref_function_pointer", GIObjectInfoUnrefFunction,
        [GIObjectInfoPtr]),
    ("get_ref_function", c_char_p, [GIObjectInfoPtr]),
    ("get_ref_function_pointer", GIObjectInfoRefFunction, [GIObjectInfoPtr]),
    ("get_set_value_function", c_char_p, [GIObjectInfoPtr]),
    ("get_set_value_function_pointer", GIObjectInfoSetValueFunction,
        [GIObjectInfoPtr]),
    ("get_get_value_function", c_char_p, [GIObjectInfoPtr]),
    ("get_get_value_function_pointer", GIObjectInfoGetValueFunction,
        [GIObjectInfoPtr]),
]

wrap_class(_gir, GIObjectInfo, GIObjectInfoPtr, "g_object_info_", _methods)

__all__ = ["GIObjectInfo", "GIObjectInfoPtr", "gi_is_object_info",
           "GIObjectInfoGetValueFunction", "GIObjectInfoRefFunction",
           "GIObjectInfoSetValueFunction", "GIObjectInfoUnrefFunction"]
