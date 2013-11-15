# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from .clib.gobject import GEnumClassPtr, GFlagsClassPtr
from .clib.ctypesutil import gicast
from .clib.gir import GIEnumInfoPtr
from .gtype import PGType
from .util import cached_property, escape_name
from .obj import add_method


class EnumBase(int):
    __gtype__ = PGType.from_name("GEnum")

EnumBase.__name__ = "GEnum"
EnumBase.__module__ = "GObject"


class _EnumClass(EnumBase):
    _allowed = {}
    _info = None

    def __get_enum_value(self):
        gtype = self.__gtype__._type
        klass = ctypes.cast(gtype.class_ref(), GEnumClassPtr)
        return klass.get_value(self).contents

    @cached_property
    def value_nick(self):
        enum_value = self.__get_enum_value()
        return enum_value.value_nick

    @cached_property
    def value_name(self):
        enum_value = self.__get_enum_value()
        return enum_value.value_name

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

FlagsBase.__name__ = "GFlags"
FlagsBase.__module__ = "GObject"


class _FlagsClass(FlagsBase):
    _flags = []
    _info = None

    @property
    def __gtype__(self):
        return PGType(self._info.g_type)

    def __get_flags_value(self, value):
        gtype = self.__gtype__._type
        klass = ctypes.cast(gtype.class_ref(), GFlagsClassPtr)
        value_ptr = klass.get_first_value(value)
        if not value_ptr:
            return
        return value_ptr.contents

    def __get_flag_values(self):
        values = []
        for (num, vname) in self._flags:
            masked = self & num
            if not masked:
                continue
            value = self.__get_flags_value(masked)
            if value:
                values.append(value)
        return values

    @cached_property
    def value_nicks(self):
        return [v.value_nick for v in self.__get_flag_values()]

    @property
    def first_value_nick(self):
        return (self.value_nicks and self.value_nicks[0]) or None

    @cached_property
    def value_names(self):
        return [v.value_name for v in self.__get_flag_values()]

    @property
    def first_value_name(self):
        return (self.value_names and self.value_names[0]) or None

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

    # add them to the class for init checks
    cls = type(info.name, _FlagsClass.__bases__, dict(_FlagsClass.__dict__))
    cls.__module__ = info.namespace

    values = _get_values(info)
    cls._flags = values
    cls._info = info

    # create instances for all of them and add to the class
    for num, vname in values:
        escaped = escape_name(vname)
        obj = cls(num)
        if escaped != vname:
            setattr(cls, escaped, obj)
        setattr(cls, vname, obj)

    return cls


def EnumAttribute(info):
    info = gicast(info, GIEnumInfoPtr)

    # add them to the class for init checks
    cls = type(info.name, _EnumClass.__bases__, dict(_EnumClass.__dict__))
    cls.__module__ = info.namespace

    values = _get_values(info)
    cls._allowed = dict(values)
    cls.__gtype__ = PGType(info.g_type)

    for method in info.get_methods():
        add_method(method, cls)

    # create instances for all of them and add to the class
    for num, vname in values:
        escaped = escape_name(vname)
        obj = cls(num)
        if escaped != vname:
            setattr(cls, escaped, obj)
        setattr(cls, vname, obj)

    return cls
