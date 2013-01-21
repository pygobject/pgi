# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast

from pgi.codegen.fieldgen import generate_field_getter
from pgi.gir import GIUnionInfoPtr, GIFieldInfoFlags
from pgi.glib import g_try_malloc0
from pgi.gtype import PGType
from pgi.obj import MethodAttribute


class _DummyInfo(object):
    def get_methods(self):
        return []


class BaseUnion(object):
    """A base class for all unions (for type checking..)"""


class _Union(BaseUnion):
    __info__ = _DummyInfo()
    __gtype__ = None
    _obj = 0
    _size = 0

    def __init_(self):
        obj = g_try_malloc0(self._size)
        if not obj and self._size:
            raise MemoryError(
                "Could not allocate structure %r" % self.__class__.__name__)
        self._obj = obj

    def __repr__(self):
        form = "<%s union at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    __str__ = __repr__


class FieldAttribute(object):
    _getter = None
    _setter = None

    def __init__(self, info):
        self._info = info


    def __get__(self, instance, owner):
        info = self._info

        if not info.flags.value & GIFieldInfoFlags.IS_READABLE:
            raise AttributeError

        if not self._getter:
            self._getter = generate_field_getter(info)

        if instance:
            return self._getter(instance)
        return self._getter

    def __set__(self, instance, value):
        if not self._info.flags.value & GIFieldInfoFlags.IS_WRITABLE:
            raise AttributeError


def UnionAttribute(info):
    union_info = cast(info, GIUnionInfoPtr)

    cls = type(info.name, _Union.__bases__, dict(_Union.__dict__))
    cls.__module__ = info.name
    cls.__gtype__ = PGType(union_info.g_type)
    cls._size = union_info.size

    # Add methods
    for method_info in union_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        setattr(cls, method_name, attr)

    # Add fields
    for field_info in union_info.get_fields():
        field_name = field_info.name
        attr = FieldAttribute(field_info)
        setattr(cls, field_name, attr)

    return cls
