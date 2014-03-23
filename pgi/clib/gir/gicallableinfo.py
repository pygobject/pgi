# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import c_char_p, POINTER, c_int

from ..glib import gint, Enum, gboolean, gchar_p, GError, Flags
from ..gobject import GSignalFlags
from .gibaseinfo import GIBaseInfo
from .gibaseinfo import GIAttributeIter, GIInfoType
from .gitypeinfo import GITypeInfo
from .giarginfo import GITransfer, GIArgInfo
from .gipropertyinfo import GIPropertyInfo
from .giargument import GIArgument
from .._utils import find_library, wrap_class
from .._compat import xrange

_gir = find_library("girepository-1.0")


@GIBaseInfo._register(GIInfoType.CALLBACK)
class GICallableInfo(GIBaseInfo):

    def get_args(self):
        for i in xrange(self.n_args):
            yield self.get_arg(i)

    def _get_repr(self):
        values = super(GICallableInfo, self)._get_repr()

        # FIXME
        #values["return_type"] = repr(self.get_return_type())
        values["caller_owns"] = repr(self.caller_owns)
        values["may_return_null"] = repr(self.may_return_null)
        values["n_args"] = repr(self.n_args)
        return values


class GIFunctionInfoFlags(Flags):
    IS_METHOD = 1 << 0
    IS_CONSTRUCTOR = 1 << 1
    IS_GETTER = 1 << 2
    IS_SETTER = 1 << 3
    WRAPS_VFUNC = 1 << 4
    THROWS = 1 << 5


class GInvokeError(Enum):
    FAILED, SYMBOL_NOT_FOUND, ARGUMENT_MISMATCH = range(3)


@GIBaseInfo._register(GIInfoType.FUNCTION)
class GIFunctionInfo(GICallableInfo):

    def _get_repr(self):
        values = super(GIFunctionInfo, self)._get_repr()

        values["symbol"] = repr(self.symbol)
        values["flags"] = repr(self.flags)
        if self.flags.value & (GIFunctionInfoFlags.IS_GETTER |
                               GIFunctionInfoFlags.IS_SETTER):
            values["property"] = repr(self.get_property())
        elif self.flags.value & GIFunctionInfoFlags.WRAPS_VFUNC:
            values["vfunc"] = repr(self.get_vfunc())

        return values


class GIVFuncInfoFlags(Enum):
    MUST_CHAIN_UP = 1 << 0
    MUST_OVERRIDE = 1 << 1
    MUST_NOT_OVERRIDE = 1 << 2


@GIBaseInfo._register(GIInfoType.VFUNC)
class GIVFuncInfo(GICallableInfo):

    def _get_repr(self):
        values = super(GIVFuncInfo, self)._get_repr()
        values["flags"] = repr(self.flags)
        values["offset"] = repr(self.offset)
        signal = self.get_signal()
        if signal:
            values["signal"] = repr(signal)
        invoker = self.get_invoker()
        if invoker:
            values["invoker"] = repr(invoker)
        return values


@GIBaseInfo._register(GIInfoType.SIGNAL)
class GISignalInfo(GICallableInfo):

    def _get_repr(self):
        values = super(GISignalInfo, self)._get_repr()
        values["flags"] = repr(self.flags)
        closure = self.get_class_closure()
        if closure:
            values["class_closure"] = repr(closure)
        values["true_stops_emit"] = repr(self.true_stops_emit)
        return values


_methods = [
    ("get_return_type", GITypeInfo, [GICallableInfo], True),
    ("get_caller_owns", GITransfer, [GICallableInfo]),
    ("may_return_null", gboolean, [GICallableInfo]),
    ("get_return_attribute", gchar_p, [GICallableInfo, gchar_p]),
    ("iterate_return_attributes", gint,
     [GICallableInfo,
      GIAttributeIter, POINTER(c_char_p), POINTER(c_char_p)]),
    ("get_n_args", gint, [GICallableInfo]),
    ("get_arg", GIArgInfo, [GICallableInfo, gint], True),
    ("load_arg", None, [GICallableInfo, gint, GIArgInfo]),
    ("load_return_type", None, [GICallableInfo, GITypeInfo]),
]

wrap_class(_gir, GICallableInfo, GICallableInfo,
           "g_callable_info_", _methods)

_methods = [
    ("get_symbol", gchar_p, [GIFunctionInfo]),
    ("get_flags", GIFunctionInfoFlags, [GIFunctionInfo]),
    ("get_property", GIPropertyInfo, [GIFunctionInfo], True),
    ("get_vfunc", GIVFuncInfo, [GIFunctionInfo], True),
    ("invoke", gboolean, [GIFunctionInfo, POINTER(GIArgument), c_int,
                          POINTER(GIArgument), c_int, POINTER(GIArgument),
                          POINTER(POINTER(GError))]),
]

wrap_class(_gir, GIFunctionInfo, GIFunctionInfo,
           "g_function_info_", _methods)

_methods = [
    ("get_flags", GIVFuncInfoFlags, [GIVFuncInfo]),
    ("get_offset", gint, [GIVFuncInfo]),
    ("get_signal", GISignalInfo, [GIVFuncInfo], True),
    ("get_invoker", GIFunctionInfo, [GIVFuncInfo], True),
]

wrap_class(_gir, GIVFuncInfo, GIVFuncInfo, "g_vfunc_info_", _methods)

_methods = [
    ("get_flags", GSignalFlags, [GISignalInfo]),
    ("get_class_closure", GIVFuncInfo, [GISignalInfo], True),
    ("true_stops_emit", gboolean, [GISignalInfo]),
]

wrap_class(_gir, GISignalInfo, GISignalInfo, "g_signal_info_", _methods)


__all__ = ["GICallableInfo", "GIFunctionInfoFlags", "GInvokeError",
           "GIFunctionInfo", "GIVFuncInfoFlags", "GIVFuncInfo",
           "GISignalInfo"]
