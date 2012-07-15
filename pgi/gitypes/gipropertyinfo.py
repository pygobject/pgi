# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gobject import GParamFlags
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr
from gitypeinfo import GITypeInfoPtr, GIInfoType
from giarginfo import GITransfer
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_property_info(base_info, _type=GIInfoType.PROPERTY):
    return base_info.get_type().value == _type


class GIPropertyInfo(GIBaseInfo):
    pass


class GIPropertyInfoPtr(GIBaseInfoPtr):
    _type_ = GIPropertyInfo

    def __repr__(self):
        values = {}
        values["flags"] = self.get_flags()
        values["type"] = self.get_type()
        values["ownership_transfer"] = self.get_ownership_transfer()
        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_flags", GParamFlags, [GIPropertyInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIPropertyInfoPtr]),
    ("get_ownership_transfer", GITransfer, [GIPropertyInfoPtr]),
]

wrap_class(_gir, GIPropertyInfo, GIPropertyInfoPtr,
           "g_property_info_", _methods)

__all__ = ["GIPropertyInfo", "GIPropertyInfoPtr", "gi_is_property_info"]
