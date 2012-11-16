# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast

from pgi.gir import GIUnionInfoPtr
from pgi.gtype import PGType


class _DummyInfo(object):
    def get_methods(self):
        return []


class _Union(object):
    __info__ = _DummyInfo()


def UnionAttribute(info, namespace, name, lib):
    struct_info = cast(info, GIUnionInfoPtr)

    cls_dict = dict(_Union.__dict__)
    g_type = struct_info.get_g_type()
    cls_dict["__gtype__"] = PGType(g_type)
    cls = type(name, _Union.__bases__, cls_dict)
    cls.__module__ = namespace

    return cls
