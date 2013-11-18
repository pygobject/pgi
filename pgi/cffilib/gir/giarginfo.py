# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .. import _create_enum_class

from ._ffi import ffi, lib
from .gibaseinfo import GIBaseInfo
from .gitypeinfo import GITypeInfo


GIDirection = _create_enum_class(ffi, "GIDirection", "GI_DIRECTION_")


GITransfer = _create_enum_class(ffi, "GITransfer", "GI_TRANSFER_")


GIScopeType = _create_enum_class(ffi, "GIScopeType", "GI_SCOPE_TYPE_")


class GIArgInfo(GIBaseInfo):

    def get_direction(self):
        return GIDirection(lib.g_arg_info_get_direction(self._ptr))

    def is_caller_allocates(self):
        return bool(lib.g_arg_info_is_caller_allocates(self._ptr))

    def is_return_value(self):
        return bool(lib.g_arg_info_is_return_value(self._ptr))

    def is_optional(self):
        return bool(lib.g_arg_info_is_optional(self._ptr))

    def may_be_null(self):
        return bool(lib.g_arg_info_may_be_null(self._ptr))

    def get_ownership_transfer(self):
        return GITransfer(lib.g_arg_info_get_ownership_transfer(self._ptr))

    def get_scope(self):
        return GIScopeType(lib.g_arg_info_get_scope(self._ptr))

    def get_closure(self):
        return lib.g_arg_info_get_closure(self._ptr)

    def get_destroy(self):
        return lib.g_arg_info_get_destroy(self._ptr)

    def get_type(self):
        return GITypeInfo(lib.g_arg_info_get_type(self._ptr))

    def load_type(self):
        # warning: lifetime bound to this info
        info = ffi.new("GITypeInfo*")
        lib.g_arg_info_load_type(self._ptr, info)
        return GITypeInfo(info)
