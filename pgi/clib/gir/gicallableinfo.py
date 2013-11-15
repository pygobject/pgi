# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import c_char_p, POINTER, c_int

from ..glib import gint, Enum, gboolean, gchar_p, GError, Flags
from ..gobject import GSignalFlags
from .gibaseinfo import GIBaseInfo, GIBaseInfoPtr
from .gibaseinfo import GIAttributeIterPtr, GIInfoType
from .gitypeinfo import GITypeInfoPtr
from .giarginfo import GITransfer, GIArgInfoPtr
from .gipropertyinfo import GIPropertyInfoPtr
from .giargument import GIArgument
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_callable_info(base_info, _it=GIInfoType):
    type_ = base_info.type.value
    return (type_ in (_it.FUNCTION, _it.CALLBACK, _it.SIGNAL, _it.VFUNC))


class GICallableInfo(GIBaseInfo):
    pass


class GICallableInfoPtr(GIBaseInfoPtr):
    _type_ = GICallableInfo

    def get_args(self):
        return map(self.get_arg, xrange(self.n_args))

    def _get_repr(self):
        values = super(GICallableInfoPtr, self)._get_repr()

        values["return_type"] = repr(self.get_return_type())
        values["caller_owns"] = repr(self.caller_owns)
        values["may_return_null"] = repr(self.may_return_null)
        values["n_args"] = repr(self.n_args)
        return values


def gi_is_function_info(base_info):
    return base_info.type.value == GIInfoType.FUNCTION


class GIFunctionInfoFlags(Flags):
    IS_METHOD = 1 << 0
    IS_CONSTRUCTOR = 1 << 1
    IS_GETTER = 1 << 2
    IS_SETTER = 1 << 3
    WRAPS_VFUNC = 1 << 4
    THROWS = 1 << 5


class GInvokeError(Enum):
    FAILED, SYMBOL_NOT_FOUND, ARGUMENT_MISMATCH = range(3)


class GIFunctionInfo(GICallableInfo):
    pass


class GIFunctionInfoPtr(GICallableInfoPtr):
    _type_ = GIFunctionInfo

    def _get_repr(self):
        values = super(GIFunctionInfoPtr, self)._get_repr()

        values["symbol"] = repr(self.symbol)
        values["flags"] = repr(self.flags)
        if self.flags.value & (GIFunctionInfoFlags.IS_GETTER |
                               GIFunctionInfoFlags.IS_SETTER):
            values["property"] = repr(self.get_property())
        elif self.flags.value & GIFunctionInfoFlags.WRAPS_VFUNC:
            values["vfunc"] = repr(self.get_vfunc())

        return values


def gi_is_vfunc_info(base_info):
    return base_info.type.value == GIInfoType.VFUNC


class GIVFuncInfoFlags(Enum):
    MUST_CHAIN_UP = 1 << 0
    MUST_OVERRIDE = 1 << 1
    MUST_NOT_OVERRIDE = 1 << 2


class GIVFuncInfo(GICallableInfo):
    pass


class GIVFuncInfoPtr(GICallableInfoPtr):
    _type_ = GIVFuncInfo

    def _get_repr(self):
        values = super(GIVFuncInfoPtr, self)._get_repr()
        values["flags"] = repr(self.flags)
        values["offset"] = repr(self.offset)
        signal = self.get_signal()
        if signal:
            values["signal"] = repr(signal)
        invoker = self.get_invoker()
        if invoker:
            values["invoker"] = repr(invoker)
        return values


def gi_is_signal_info(base_info):
    return base_info.type.value == GIInfoType.SIGNAL


class GISignalInfo(GICallableInfo):
    pass


class GISignalInfoPtr(GICallableInfoPtr):
    _type_ = GISignalInfo

    def _get_repr(self):
        values = super(GISignalInfoPtr, self)._get_repr()
        values["flags"] = repr(self.flags)
        closure = self.get_class_closure()
        if closure:
            values["class_closure"] = repr(closure)
        values["true_stops_emit"] = repr(self.true_stops_emit)
        return values


_methods = [
    ("get_return_type", GITypeInfoPtr, [GICallableInfoPtr], True),
    ("get_caller_owns", GITransfer, [GICallableInfoPtr]),
    ("may_return_null", gboolean, [GICallableInfoPtr]),
    ("get_return_attribute", gchar_p, [GICallableInfoPtr, gchar_p]),
    ("iterate_return_attributes", gint,
     [GICallableInfoPtr,
      GIAttributeIterPtr, POINTER(c_char_p), POINTER(c_char_p)]),
    ("get_n_args", gint, [GICallableInfoPtr]),
    ("get_arg", GIArgInfoPtr, [GICallableInfoPtr, gint], True),
    ("load_arg", None, [GICallableInfoPtr, gint, GIArgInfoPtr]),
    ("load_return_type", None, [GICallableInfoPtr, GITypeInfoPtr]),
]

wrap_class(_gir, GICallableInfo, GICallableInfoPtr,
           "g_callable_info_", _methods)

_methods = [
    ("get_symbol", gchar_p, [GIFunctionInfoPtr]),
    ("get_flags", GIFunctionInfoFlags, [GIFunctionInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIFunctionInfoPtr], True),
    ("get_vfunc", GIVFuncInfoPtr, [GIFunctionInfoPtr], True),
    ("invoke", gboolean, [GIFunctionInfoPtr, POINTER(GIArgument), c_int,
                          POINTER(GIArgument), c_int, POINTER(GIArgument),
                          POINTER(POINTER(GError))]),
]

wrap_class(_gir, GIFunctionInfo, GIFunctionInfoPtr,
           "g_function_info_", _methods)

_methods = [
    ("get_flags", GIVFuncInfoFlags, [GIVFuncInfoPtr]),
    ("get_offset", gint, [GIVFuncInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIVFuncInfoPtr], True),
    ("get_invoker", GIFunctionInfoPtr, [GIVFuncInfoPtr], True),
]

wrap_class(_gir, GIVFuncInfo, GIVFuncInfoPtr, "g_vfunc_info_", _methods)

_methods = [
    ("get_flags", GSignalFlags, [GISignalInfoPtr]),
    ("get_class_closure", GIVFuncInfoPtr, [GISignalInfoPtr], True),
    ("true_stops_emit", gboolean, [GISignalInfoPtr]),
]

wrap_class(_gir, GISignalInfo, GISignalInfoPtr, "g_signal_info_", _methods)


__all__ = ["GICallableInfo", "GICallableInfoPtr", "gi_is_callable_info",
           "GIFunctionInfoFlags", "GInvokeError", "GIFunctionInfo",
           "GIFunctionInfoPtr", "GIVFuncInfoFlags", "GIVFuncInfo",
           "GIVFuncInfoPtr", "GISignalInfo", "GISignalInfoPtr",
           "gi_is_function_info", "gi_is_signal_info", "gi_is_vfunc_info"]
