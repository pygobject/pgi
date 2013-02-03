# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.gobject import GEnumClassPtr
from pgi.ctypesutil import gicast
from pgi.gir import GIEnumInfoPtr
from pgi.gtype import PGType
from pgi.util import cached_property


class EnumBase(int):
    pass


class _EnumClass(EnumBase):
    _allowed = {}
    _info = None

    @property
    def __gtype__(self):
        return PGType(self._info.g_type)

    @property
    def __enum_value(self):
        gtype = self.__gtype__._type
        klass = ctypes.cast(gtype.class_ref(), GEnumClassPtr)
        return klass.get_value(self)

    @cached_property
    def value_nick(self):
        enum_value = self.__enum_value
        return enum_value.contents.value_nick

    @cached_property
    def value_name(self):
        enum_value = self.__enum_value
        return enum_value.contents.value_name

    def __new__(cls, value):
        if not isinstance(value, (long, int)):
            raise TypeError("int expected, got %r instead" % type(value))
        instance = int.__new__(cls, value)
        if value in cls._allowed:
            return instance
        raise ValueError("invalid enum value: %r", value)

    def __repr__(self):
        return "<enum %s of type %s>" % (self._allowed[self],
                                         self.__class__.__name__)

    __str__ = __repr__


class FlagsBase(int):
    pass


class _FlagsClass(FlagsBase):
    _flags = []
    __gtype__ = None

    def __new__(cls, value):
        if not isinstance(value, (long, int)):
            raise TypeError("int expected, got %r instead" % type(value))
        return int.__new__(cls, value)

    def __repr__(self):
        names = []
        for (num, vname) in self._flags:
            if not self and not num:
                names.append(vname)
                break
            if self & num:
                names.append(vname)

        names = " | ".join(names) or "0"
        return "<flags %s of type %s>" % (names, self.__class__.__name__)

    __str__ = __repr__

    def __or__(self, other):
        return type(self)(int(self) | other)

    def __and__(self, other):
        return type(self)(int(self) & other)


def _get_values(enum):
    values = []

    for value in enum.get_values():
        num = value.value
        vname = value.name.upper()
        values.append((num, vname))

    return values


def FlagsAttribute(info):
    info = gicast(info, GIEnumInfoPtr)
    enum_name = info.type_name or info.name

    # add them to the class for init checks
    cls = type(enum_name, _FlagsClass.__bases__, dict(_FlagsClass.__dict__))

    values = _get_values(info)
    cls._flags = values
    cls.__gtype__ = PGType(info.g_type)

    # create instances for all of them and add to the class
    for num, vname in values:
        setattr(cls, vname, cls(num))

    return cls


class _EnumMethod(object):
    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        raise NotImplementedError("%r not supported" % self._name)


def EnumAttribute(info):
    info = gicast(info, GIEnumInfoPtr)
    enum_name = info.namespace + info.name

    # add them to the class for init checks
    cls = type(enum_name, _EnumClass.__bases__, dict(_EnumClass.__dict__))

    values = _get_values(info)
    cls._allowed = dict(values)
    cls._info = info

    for method in info.get_methods():
        name = method.name
        setattr(cls, name, _EnumMethod(name))

    # create instances for all of them and add to the class
    for num, vname in values:
        setattr(cls, vname, cls(num))

    return cls
