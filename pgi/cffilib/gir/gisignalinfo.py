# Copyright 2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ._ffi import lib
from .gibaseinfo import GIBaseInfo, GIInfoType
from .gicallableinfo import GICallableInfo


@GIBaseInfo._register(GIInfoType.SIGNAL)
class GISignalInfo(GICallableInfo):

    @property
    def flags(self):
        return lib.g_signal_info_get_flags(self._ptr)

    @property
    def true_stops_emit(self):
        return lib.g_signal_info_true_stops_emit(self._ptr)
