# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast
from gitypes import GICallableInfoPtr, GIFunctionInfoPtr, GITypeTag
from gitypes.glib import *

from util import typeinfo_to_ctypes


def get_array(info, value):
    r = []
    if not value:
        return r
    if info.is_zero_terminated():
        i = 0
        x = value[i]
        while x:
            r.append(x)
            i += 1
            x = value[i]
    return r


def handle_return(return_info, value):
    tag = return_info.get_tag().value
    ptr = return_info.is_pointer()

    if tag == GITypeTag.UTF8:
        return value
    elif tag == GITypeTag.ARRAY:
        return get_array(return_info, value)
    else:
        return value


class Function(object):
    _handle = None
    _return_info = None

    def __init__(self, info, lib):
        call_info = cast(info, GICallableInfoPtr)
        return_info = call_info.get_return_type()
        tag = return_info.get_tag()
        func = cast(call_info, GIFunctionInfoPtr)

        h = getattr(lib, func.get_symbol())
        h.restype = typeinfo_to_ctypes(return_info)
        h.argtypes = tuple()

        self._handle = h
        self._return_info = return_info

    def __call__(self, *args):
        value = self._handle()
        return handle_return(self._return_info, value)


def FunctionAttribute(info, namespace, name, lib):
    return type(name, Function.__bases__, dict(Function.__dict__))(info, lib)
