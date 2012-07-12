# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast

from gitypes import GIStructInfoPtr, GIBaseInfoPtr, GIFunctionInfoFlags
from gitypes import GIRegisteredTypeInfoPtr

from obj import _ClassMethodAttribute
from gtype import PGType


class _Structure(object):
    _obj = None
    __gtype__ = None

    def __init__(self, *args, **kwargs):
        raise TypeError


def StructureAttribute(info, namespace, name, lib):
    reg_info = cast(info, GIRegisteredTypeInfoPtr)
    struct_info = cast(info, GIStructInfoPtr)

    cls_dict = dict(_Structure.__dict__)
    g_type = reg_info.get_g_type()
    cls_dict["__gtype__"] = PGType(g_type)
    cls = type(name, _Structure.__bases__, cls_dict)
    cls.__module__ = namespace

    for i in xrange(struct_info.get_n_methods()):
        func_info = struct_info.get_method(i)
        func_flags = func_info.get_flags().value

        base_info = cast(func_info, GIBaseInfoPtr)

        if func_flags == 0 or func_flags == GIFunctionInfoFlags.IS_METHOD:
            mname = base_info.get_name()
            attr = _ClassMethodAttribute(base_info, namespace, mname, lib)
            setattr(cls, mname, attr)
        else:
            base_info.unref()

    return cls
