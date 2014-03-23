# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .. import _create_enum_class, glib
from .._compat import PY3
from ._ffi import ffi, lib
from .gibaseinfo import GIBaseInfo, GIInfoType
from .gicallableinfo import GICallableInfo
from .gipropertyinfo import GIPropertyInfo


GIFunctionInfoFlags = _create_enum_class(ffi, "GIFunctionInfoFlags",
                                         "GI_FUNCTION_")


GInvokeError = _create_enum_class(ffi, "GInvokeError", "G_INVOKE_ERROR_")


@GIBaseInfo._register(GIInfoType.FUNCTION)
class GIFunctionInfo(GICallableInfo):
    # FIXME: everything here..

    @property
    def symbol(self):
        res = lib.g_function_info_get_symbol(self._ptr)
        res = ffi.string(res)
        if PY3:
            res = res.decode("ascii")
        return res

    @property
    def flags(self):
        return GIFunctionInfoFlags(lib.g_function_info_get_flags(self._ptr))

    def get_property(self):
        res = lib.g_function_info_get_property(self._ptr)
        if res:
            return GIPropertyInfo(res)

    def invoke(self, in_args, out_args, return_value):
        if return_value is None:
            return_value = ffi.NULL
        if in_args is None:
            in_args = ffi.NULL
            n_in_args = 0
        else:
            n_in_args = len(in_args)
        if out_args is None:
            out_args = ffi.NULL
            n_out_args = 0
        else:
            n_out_args = len(out_args)
        with glib.gerror() as error:
            res = lib.g_function_info_invoke(
                self._ptr, in_args, n_in_args, out_args, n_out_args,
                return_value, error)
        return bool(res)
