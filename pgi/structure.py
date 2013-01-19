# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast

from pgi.gir import GIStructInfoPtr
from pgi.glib import g_try_malloc0
from pgi.obj import MethodAttribute
from pgi.gtype import PGType


class BaseStructure(object):
    """A base class for all structs (for type checking..)"""


class _Structure(BaseStructure):
    """Class template for structures."""

    _obj = None  # the address of the struct
    _size = 0 # size fo the struct in bytes
    __gtype__ = None  # the gtype

    def __init__(self):
        obj = g_try_malloc0(self._size)
        if not obj and self._size:
            raise MemoryError(
                "Could not allocate structure %r" % self.__class__.__name__)
        self._obj = obj

    def __repr__(self):
        form = "<%s structure at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    __str__ = __repr__


def StructureAttribute(info):
    """Creates a new struct class."""

    struct_info = cast(info, GIStructInfoPtr)

    # Copy the template and add the gtype
    cls_dict = dict(_Structure.__dict__)
    cls = type(info.name, _Structure.__bases__, cls_dict)
    cls.__module__ = info.namespace
    cls.__gtype__ = PGType(struct_info.g_type)
    cls._size = struct_info.size

    # Add methods
    for method_info in struct_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        if attr:
            setattr(cls, method_name, attr)

    return cls
