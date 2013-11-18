# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ._ffi import lib
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from .gibaseinfo import GIBaseInfo, GIInfoType
from .gifunctioninfo import GIFunctionInfo
from .gipropertyinfo import GIPropertyInfo


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
    def n_properties(self):
        return lib.g_object_info_get_n_properties(self._ptr)

    def get_property(self, n):
        return GIPropertyInfo(lib.g_object_info_get_property(self._ptr, n))

    def get_properties(self):
        for i in xrange(self.n_properties):
            yield self.get_property(i)
