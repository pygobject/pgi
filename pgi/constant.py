# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from warnings import warn
from ctypes import cast, byref

from gitypes import GIBaseInfoPtr, GIConstantInfoPtr, GIArgument


_union_access = [None, "v_boolean", "v_int8", "v_uint8", "v_int16",
                 "v_uint16", "v_int32", "v_uint32", "v_int64", "v_uint64",
                 "v_float", "v_double", None, "v_string", "v_string",
                 None, None, None, None, None, None, None]


def ConstantAttribute(info, namespace, name, lib):
    const = cast(info, GIConstantInfoPtr)

    arg = GIArgument()
    const.get_value(byref(arg))

    const_type = const.get_type()
    tag_type = const_type.get_tag().value
    cast(const_type, GIBaseInfoPtr).unref()

    value_member = _union_access[tag_type]
    if not value_member:
        warn("Not supported const type", Warning)
        value = None
    else:
        value = getattr(arg, value_member)

    return value
