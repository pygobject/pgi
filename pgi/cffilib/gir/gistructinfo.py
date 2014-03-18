# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .._compat import xrange
from ._ffi import lib
from .gibaseinfo import GIBaseInfo, GIInfoType
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from .gifieldinfo import GIFieldInfo


@GIBaseInfo._register(GIInfoType.STRUCT)
class GIStructInfo(GIRegisteredTypeInfo):

    @property
    def n_fields(self):
        return lib.g_struct_info_get_n_fields(self._ptr)

    def get_field(self, n):
        return GIFieldInfo(lib.g_struct_info_get_field(self._ptr, n))

    def get_fields(self):
        for i in xrange(self.n_fields):
            yield self.get_field(i)
