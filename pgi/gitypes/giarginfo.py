# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gitypeinfo import *
from gibaseinfo import *
from _util import wrap_class, load

_gir = load("girepository-1.0")


def gi_is_arg_info(base_info):
    return base_info.get_type().value == GIInfoType.ARG


class GITransfer(Enum):
    NOTHING, CONTAINER, EVERYTHING = range(3)


class GIDirection(Enum):
    IN, OUT, INOUT = range(3)


class GIScopeType(Enum):
    INVALID, CALL, ASYNC, NOTIFIED = range(4)


class GIArgInfo(GIBaseInfo):
    pass


class GIArgInfoPtr(POINTER(GIArgInfo)):
    _type_ = GIArgInfo

    def __repr__(self):
        values = {}
        values["direction"] = self.get_direction()
        values["is_caller_allocates"] = self.is_caller_allocates()
        values["is_return_value"] = self.is_return_value()
        values["is_optional"] = self.is_optional()
        values["may_be_null"] = self.may_be_null()
        values["ownership_transfer"] = self.get_ownership_transfer()
        values["scope"] = self.get_scope()
        values["closure"] = self.get_closure()
        values["destroy"] = self.get_destroy()
        values["type"] = self.get_type()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_direction", GIDirection, [GIArgInfoPtr]),
    ("is_caller_allocates", gboolean, [GIArgInfoPtr]),
    ("is_return_value", gboolean, [GIArgInfoPtr]),
    ("is_optional", gboolean, [GIArgInfoPtr]),
    ("may_be_null", gboolean, [GIArgInfoPtr]),
    ("get_ownership_transfer", GITransfer, [GIArgInfoPtr]),
    ("get_scope", GIScopeType, [GIArgInfoPtr]),
    ("get_closure", gint, [GIArgInfoPtr]),
    ("get_destroy", gint, [GIArgInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIArgInfoPtr]),
    ("load_type", None, [GIArgInfoPtr, GITypeInfoPtr]),
]

wrap_class(_gir, GIArgInfo, GIArgInfoPtr, "g_arg_info_", _methods)

__all__ = ["GITransfer", "GIDirection", "GIScopeType", "GIArgInfo",
           "GIArgInfoPtr", "gi_is_arg_info"]
