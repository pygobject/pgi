# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import *

from glib import *
from gobject import *
from gibaseinfo import *
from gitypeinfo import *
from giarginfo import *
from gipropertyinfo import *
from giargument import *
from _util import load, wrap_class

_gir = load("girepository-1.0")

# Definitions & Helpers:
# ----------------------

# GICallableInfo


def gi_is_callable_info(base_info):
    type_ = base_info.get_type().value
    it = GIInfoType
    return (type_ in (it.FUNCTION, it.CALLBACK, it.SIGNAL, it.VFUNC))


class GICallableInfo(GIBaseInfo):
    pass


class GICallableInfoPtr(POINTER(GICallableInfo)):
    _type_ = GICallableInfo

# GIFunctionInfo


def gi_is_function_info(base_info):
    return base_info.get_type().value == GIInfoType.FUNCTION


class GIFunctionInfoFlags(guint):
    IS_METHOD = 1 << 0
    IS_CONSTRUCTOR = 1 << 1
    IS_GETTER = 1 << 2
    IS_SETTER = 1 << 3
    WRAPS_VFUNC = 1 << 4
    THROWS = 1 << 5


class GInvokeError(guint):
    FAILED, SYMBOL_NOT_FOUND, ARGUMENT_MISMATCH = range(3)


class GIFunctionInfo(GIBaseInfo):
    pass


class GIFunctionInfoPtr(POINTER(GIFunctionInfo)):
    _type_ = GIFunctionInfo

# GIVFuncInfo


def gi_is_vfunc_info(base_info):
    return base_info.get_type().value == GIInfoType.VFUNC


class GIVFuncInfoFlags(guint):
    MUST_CHAIN_UP = 1 << 0
    MUST_OVERRIDE = 1 << 1
    MUST_NOT_OVERRIDE = 1 << 2


class GIVFuncInfo(GIBaseInfo):
    pass


class GIVFuncInfoPtr(POINTER(GIVFuncInfo)):
    _type_ = GIVFuncInfo

# GISignalInfo


def gi_is_signal_info(base_info):
    return base_info.get_type().value == GIInfoType.SIGNAL


class GISignalInfo(GIBaseInfo):
    pass


class GISignalInfoPtr(POINTER(GISignalInfo)):
    _type_ = GISignalInfo

# Functions:
# ----------

# GICallableInfo

_methods = [
    ("get_return_type", GITypeInfoPtr, [GICallableInfoPtr]),
    ("get_caller_owns", GITransfer, [GICallableInfoPtr]),
    ("may_return_null", gboolean, [GICallableInfoPtr]),
    ("get_return_attribute", gchar_p, [GICallableInfoPtr, gchar_p]),
    ("iterate_return_attributes", gint, [GICallableInfoPtr,
        POINTER(GIAttributeIter), POINTER(c_char_p), POINTER(c_char_p)]),
    ("get_n_args", gint, [GICallableInfoPtr]),
    ("get_arg", GIArgInfoPtr, [GICallableInfoPtr, gint]),
    ("load_arg", None, [GICallableInfoPtr, gint, GIArgInfoPtr]),
    ("load_return_type", None, [GICallableInfoPtr, GITypeInfoPtr]),
]

wrap_class(_gir, GICallableInfo, GICallableInfoPtr,
           "g_callable_info_", _methods)

# GIFunctionInfo

_methods = [
    ("get_symbol", gchar_p, [GIFunctionInfoPtr]),
    ("get_flags", GIFunctionInfoFlags, [GIFunctionInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIFunctionInfoPtr]),
    ("get_vfunc", GIVFuncInfoPtr, [GIFunctionInfoPtr]),
    ("invoke", gboolean, [GIFunctionInfoPtr, POINTER(GIArgument), c_int,
                          POINTER(GIArgument), c_int, POINTER(GIArgument),
                          POINTER(POINTER(GError))]),
]

wrap_class(_gir, GIFunctionInfo, GIFunctionInfoPtr,
           "g_function_info_", _methods)

# GIVFuncInfo

_methods = [
    ("get_flags", GIVFuncInfoFlags, [GIVFuncInfoPtr]),
    ("get_offset", gint, [GIVFuncInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIVFuncInfoPtr]),
    ("get_invoker", GIFunctionInfoPtr, [GIVFuncInfoPtr]),
]

wrap_class(_gir, GIVFuncInfo, GIVFuncInfoPtr, "g_vfunc_info_", _methods)

# GISignalInfo

_methods = [
    ("get_flags", GSignalFlags, [GISignalInfoPtr]),
    ("get_class_closure", GIVFuncInfoPtr, [GISignalInfoPtr]),
    ("true_stops_emit", gboolean, [GISignalInfoPtr]),
]

wrap_class(_gir, GISignalInfo, GISignalInfoPtr, "g_signal_info_", _methods)


__all__ = ["GICallableInfo", "GICallableInfoPtr", "gi_is_callable_info",
           "GIFunctionInfoFlags", "GInvokeError", "GIFunctionInfo",
           "GIFunctionInfoPtr", "GIVFuncInfoFlags", "GIVFuncInfo",
           "GIVFuncInfoPtr", "GISignalInfo", "GISignalInfoPtr",
           "gi_is_function_info", "gi_is_signal_info", "gi_is_vfunc_info"]
