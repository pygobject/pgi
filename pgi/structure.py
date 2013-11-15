# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .clib.ctypesutil import gicast, memcpy
from .codegen.fieldgen import generate_field_getter, generate_field_setter
from .clib.gir import GIUnionInfoPtr, GIFieldInfoFlags, GIStructInfoPtr
from .clib.glib import g_try_malloc0, free
from .gtype import PGType
from .obj import add_method


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
    _needs_free = False

    def __init__(self):
        obj = g_try_malloc0(self._size)
        if not obj and self._size:
            raise MemoryError(
                "Could not allocate structure %r" % self.__class__.__name__)
        self._obj = obj
        self._needs_free = True

    def __repr__(self):
        form = "<%s union at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    __str__ = __repr__

    def __del__(self):
        if self._needs_free:
            free(self._obj)


class BaseStructure(object):
    """A base class for all structs (for type checking..)"""


class _Structure(BaseStructure):
    """Class template for structures."""

    _obj = 0
    _size = 0
    __gtype__ = None
    _needs_free = False
    _is_gtype_struct = False

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

    def copy(self):
        new = type(self)()
        memcpy(new._obj, self._obj, self._size)
        new._needs_free = True
        return new

    __str__ = __repr__

    def __del__(self):
        if self._needs_free:
            free(self._obj)


class FieldAttribute(object):
    _getter = None
    _setter = None

    def __init__(self, info):
        self._info = info
        self._readable = info.flags.value & GIFieldInfoFlags.IS_READABLE
        self._writeable = info.flags.value & GIFieldInfoFlags.IS_WRITABLE

    def __get__(self, instance, owner):
        if not self._readable:
            raise AttributeError

        if not self._getter:
            self._getter = generate_field_getter(self._info)

        if instance:
            return self._getter(instance)
        return self

    def __set__(self, instance, value):
        if not self._writeable:
            raise AttributeError

        if not self._setter:
            self._setter = generate_field_setter(self._info)

        if instance:
            return self._setter(instance, value)
        return self


def UnionAttribute(union_info):
    union_info = gicast(union_info, GIUnionInfoPtr)

    cls = type(union_info.name, _Union.__bases__, dict(_Union.__dict__))
    cls.__module__ = union_info.namespace
    cls.__gtype__ = PGType(union_info.g_type)
    cls._size = union_info.size

    # Add methods
    for method_info in union_info.get_methods():
        add_method(method_info, cls)

    # Add fields
    for field_info in union_info.get_fields():
        field_name = field_info.name
        attr = FieldAttribute(field_info)
        setattr(cls, field_name, attr)

    return cls


def StructureAttribute(struct_info):
    """Creates a new struct class."""

    struct_info = gicast(struct_info, GIStructInfoPtr)

    # Copy the template and add the gtype
    cls_dict = dict(_Structure.__dict__)
    cls = type(struct_info.name, _Structure.__bases__, cls_dict)
    cls.__module__ = struct_info.namespace
    cls.__gtype__ = PGType(struct_info.g_type)
    cls._size = struct_info.size
    cls._is_gtype_struct = struct_info.is_gtype_struct

    # Add methods
    for method_info in struct_info.get_methods():
        add_method(method_info, cls)

    # Add fields
    for field_info in struct_info.get_fields():
        field_name = field_info.name
        attr = FieldAttribute(field_info)
        setattr(cls, field_name, attr)

    return cls
