# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.ctypesutil import gicast
from pgi.gir import GIEnumInfoPtr
from pgi.gtype import PGType


class _EnumClass(int):
    _allowed = {}
    __gtype__ = None

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


class _FlagsClass(int):
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

    values = _get_values(info)

    # add them to the class for init checks
    cls_dict = dict(_FlagsClass.__dict__)
    cls_dict["_flags"] = values
    cls = type(enum_name, _FlagsClass.__bases__, cls_dict)

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
    enum_name = info.type_name or info.name

    values = _get_values(info)

    # add them to the class for init checks
    cls_dict = dict(_EnumClass.__dict__)
    cls_dict["_allowed"] = dict(values)
    cls = type(enum_name, _EnumClass.__bases__, cls_dict)

    cls.__gtype__ = PGType(info.g_type)

    for method in info.get_methods():
        name = method.name
        setattr(cls, name, _EnumMethod(name))

    # create instances for all of them and add to the class
    for num, vname in values:
        setattr(cls, vname, cls(num))

    return cls
