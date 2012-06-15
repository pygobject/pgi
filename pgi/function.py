# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast
from gitypes import GICallableInfoPtr, GIFunctionInfoPtr, GITypeTag
from gitypes.glib import *


class array_return(object):
    def __init__(self, info):
        self.zero = info.is_zero_terminated()

    def convert(self, p):
        r = []
        if not p:
            return r
        if self.zero:
            i = 0
            x = p[i]
            while x:
                r.append(x)
                i += 1
                x = p[i]
        return r


def gtypeinfo_to_ctypes(info):
    tag = info.get_tag().value
    ptr = info.is_pointer()

    if ptr:
        if tag == GITypeTag.UTF8:
            return gchar_p
        elif tag == GITypeTag.VOID:
            return None
        elif tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
    else:
        if tag == GITypeTag.BOOLEAN:
            return gboolean
        elif tag == GITypeTag.UINT32:
            return guint32
        elif tag == GITypeTag.VOID:
            return


class Function(object):
    _handle = None
    _convert = None

    def __init__(self, info, lib):
        info = cast(info, GICallableInfoPtr)
        return_info = info.get_return_type()
        tag = return_info.get_tag()
        func = cast(info, GIFunctionInfoPtr)

        h = getattr(lib, func.get_symbol())
        h.restype = gtypeinfo_to_ctypes(return_info)
        h.argtypes = []

        if tag.value == GITypeTag.ARRAY:
            self._convert = array_return(return_info)
        self._handle = h

    def __call__(self, *args):
        r = self._handle()
        if self._convert:
            return self._convert.convert(r)
        return r


def FunctionAttribute(info, namespace, name, lib):
    return type(name, Function.__bases__, dict(Function.__dict__))(info, lib)
