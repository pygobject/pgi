# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast

from pgi.gir import GIFunctionInfoPtr, GITypeTag
from pgi.glib import gpointer
from pgi.util import typeinfo_to_ctypes


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
    #ptr = return_info.is_pointer()

    if tag == GITypeTag.UTF8:
        return value
    elif tag == GITypeTag.ARRAY:
        return get_array(return_info, value)
    else:
        return value


class Function(object):
    _handle = None
    _return_info = None
    _is_function = True

    def __init__(self, info, lib):
        func_info = cast(info, GIFunctionInfoPtr)
        return_info = func_info.get_return_type()
        #tag = return_info.get_tag()

        h = getattr(lib, func_info.get_symbol())
        h.restype = typeinfo_to_ctypes(return_info)
        h.argtypes = tuple([gpointer, gpointer])

        self._handle = h
        self._return_info = return_info

    def __call__(self, *args):
        value = self._handle(0, 0)
        return handle_return(self._return_info, value)


def FunctionAttribute(info, namespace, name, lib):
    return type(name, Function.__bases__, dict(Function.__dict__))(info, lib)
