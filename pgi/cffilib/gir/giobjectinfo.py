# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange, PY3
from ._ffi import ffi, lib
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from .gibaseinfo import GIBaseInfo, GIInfoType
from .gifunctioninfo import GIFunctionInfo
from .gipropertyinfo import GIPropertyInfo
from .gifieldinfo import GIFieldInfo
from .giconstantinfo import GIConstantInfo


@GIBaseInfo._register(GIInfoType.OBJECT)
class GIObjectInfo(GIRegisteredTypeInfo):

    @property
    def n_methods(self):
        return lib.g_object_info_get_n_methods(self._ptr)

    def get_method(self, n):
        return GIFunctionInfo(lib.g_object_info_get_method(self._ptr, n))

    def get_methods(self):
        for i in xrange(self.n_methods):
            yield self.get_method(i)

    @property
    def n_fields(self):
        return lib.g_object_info_get_n_fields(self._ptr)

    def get_field(self, n):
        return GIFieldInfo(lib.g_object_info_get_field(self._ptr, n))

    def get_fields(self):
        for i in xrange(self.n_fields):
            yield self.get_field(i)

    @property
    def n_constants(self):
        return lib.g_object_info_get_n_constants(self._ptr)

    def get_constant(self, n):
        return GIConstantInfo(lib.g_object_info_get_constant(self._ptr, n))

    def get_constants(self):
        for i in xrange(self.n_constants):
            yield self.get_constant(i)

    @property
    def n_vfuncs(self):
        return lib.g_object_info_get_n_vfuncs(self._ptr)

    def get_vfunc(self, n):
        return GIFunctionInfo(lib.g_object_info_get_vfunc(self._ptr, n))

    def get_vfuncs(self):
        for i in xrange(self.n_vfuncs):
            yield self.get_vfunc(i)

    @property
    def n_signals(self):
        return lib.g_object_info_get_n_signals(self._ptr)

    def get_signal(self, n):
        return GIFunctionInfo(lib.g_object_info_get_signal(self._ptr, n))

    def get_signals(self):
        for i in xrange(self.n_signals):
            yield self.get_signal(i)

    @property
    def n_interfaces(self):
        return lib.g_object_info_get_n_interfaces(self._ptr)

    def get_interface(self, n):
        return GIFunctionInfo(lib.g_object_info_get_interface(self._ptr, n))

    def get_interfaces(self):
        for i in xrange(self.n_interfaces):
            yield self.get_interface(i)

    @property
    def n_properties(self):
        return lib.g_object_info_get_n_properties(self._ptr)

    def get_property(self, n):
        return GIPropertyInfo(lib.g_object_info_get_property(self._ptr, n))

    def get_properties(self):
        for i in xrange(self.n_properties):
            yield self.get_property(i)

    @property
    def type_name(self):
        res = ffi.string(lib.g_object_info_get_type_name(self._ptr))
        if PY3:
            res = res.decode("ascii")
        return res

    @property
    def type_init(self):
        res = ffi.string(lib.g_object_info_get_type_init(self._ptr))
        if PY3:
            res = res.decode("ascii")
        return res
