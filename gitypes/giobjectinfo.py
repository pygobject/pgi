# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER, c_char_p, CFUNCTYPE, c_void_p

from glib import *
from gobject import *
from gibaseinfo import *
from giinterfaceinfo import *
from gifieldinfo import *
from gipropertyinfo import *
from gicallableinfo import *
from giconstantinfo import *
from gistructinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_object_info(base_info):
    return base_info.get_type().value == GIInfoType.OBJECT


class GIObjectInfo(GIBaseInfo):
    pass


class GIObjectInfoPtr(POINTER(GIObjectInfo)):
    _type_ = GIObjectInfo

GIObjectInfoGetValueFunction = CFUNCTYPE(c_void_p, POINTER(GValue))
GIObjectInfoRefFunction = CFUNCTYPE(c_void_p, c_void_p)
GIObjectInfoSetValueFunction = CFUNCTYPE(None, POINTER(GValue), c_void_p)
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
