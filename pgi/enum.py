# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast

from pgi.gir import GIEnumInfoPtr


class _EnumClass(int):
    _allowed = {}

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

    def __new__(cls, value):
        if not isinstance(value, (long, int)):
            raise TypeError("int expected, got %r instead" % type(value))
        return int.__new__(cls, value)

    def __repr__(self):
        names = []
        for (num, vname) in self._flags:
            if self & num:
                names.append(vname)

        names = " | ".join(names) or "0"
        return "<flags %s of type %s>" % (names, self.__class__.__name__)

    __str__ = __repr__


def _get_values(enum):
    values = []

    for value in enum.get_values():
        num = value.get_value()
        vname = value.get_name().upper()
        value.unref()
        values.append((num, vname))

    return values


def FlagsAttribute(info, namespace, name, lib):
    enum = cast(info, GIEnumInfoPtr)
    enum_name = enum.get_type_name()

    values = _get_values(enum)

    # add them to the class for init checks
    cls_dict = dict(_FlagsClass.__dict__)
    cls_dict["_flags"] = values
    cls = type(enum_name, _FlagsClass.__bases__, cls_dict)

    # create instances for all of them and add to the class
    for num, vname in values:
        setattr(cls, vname, cls(num))

    return cls


class _EnumMethod(object):
    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        raise NotImplementedError("%r not supported" % self._name)


def EnumAttribute(info, namespace, name, lib):
    enum = cast(info, GIEnumInfoPtr)
    enum_name = enum.get_type_name()

    values = _get_values(enum)

    # add them to the class for init checks
    cls_dict = dict(_EnumClass.__dict__)
    cls_dict["_allowed"] = dict(values)
    cls = type(enum_name, _EnumClass.__bases__, cls_dict)

    for method in enum.get_methods():
        name = method.get_name()
        setattr(cls, name, _EnumMethod(name))
        method.unref()

    # create instances for all of them and add to the class
    for num, vname in values:
        setattr(cls, vname, cls(num))

    return cls
