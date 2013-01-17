# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

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
    g_type = struct_info.g_type
    cls_dict["__gtype__"] = PGType(g_type)
    cls = type(name, _Union.__bases__, cls_dict)
    cls.__module__ = namespace

    return cls
