# Copyright 2012,2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from .gtype import PGType as GType
from .enum import EnumBase as GEnum
from .enum import FlagsBase as GFlags
from .gerror import PGError as GError
from .obj import InterfaceBase as GInterface
from .properties import list_properties
from . import version_info as pygobject_version


GType, GEnum, GFlags, GError, GInterface, list_properties, pygobject_version

GBoxed = None
GObject = None
GObjectWeakRef = None
GParamSpec = None
GPointer = None
Warning = None
TYPE_INVALID = None

features = {'generic-c-marshaller': True}


def _gvalue_set(self, boxed):
    # XXX
    return type(self).__mro__[1].set_boxed(self, boxed)


def _gvalue_get(self):
    # XXX
    return type(self).__mro__[1].get_boxed(self)


def type_register(*args, **kwargs):
    raise NotImplementedError


def new(gtype_or_similar):
    return GType(gtype_or_similar).pytype()


def _min_value(ctypes_type):
    signed = ctypes_type(-1).value == -1
    if signed:
        return - 2 ** (ctypes.sizeof(ctypes_type) * 8 - 1)
    return 0


def _max_value(ctypes_type):
    signed = ctypes_type(-1).value == -1
    return 2 ** (ctypes.sizeof(ctypes_type) * 8 - signed) - 1


G_MINDOUBLE = 2.2250738585072014e-308
G_MAXDOUBLE = 1.7976931348623157e+308
G_MINFLOAT = 1.1754943508222875e-38
G_MAXFLOAT = 3.4028234663852886e+38
G_MINSHORT = _min_value(ctypes.c_short)
G_MAXSHORT = _max_value(ctypes.c_short)
G_MAXUSHORT = _max_value(ctypes.c_ushort)
G_MININT = _min_value(ctypes.c_int)
G_MAXINT = _max_value(ctypes.c_int)
G_MAXUINT = _max_value(ctypes.c_uint)
G_MINLONG = _min_value(ctypes.c_long)
G_MAXLONG = _max_value(ctypes.c_long)
G_MAXULONG = _max_value(ctypes.c_ulong)
G_MAXSIZE = _max_value(ctypes.c_size_t)
G_MINSSIZE = _min_value(ctypes.c_ssize_t)
G_MAXSSIZE = _max_value(ctypes.c_ssize_t)
G_MINOFFSET = _min_value(ctypes.c_int64)
G_MAXOFFSET = _max_value(ctypes.c_int64)


class OptionContext(object):

    def __init__(*args, **kwargs):
        raise NotImplementedError


class OptionGroup(object):

    def __init__(*args, **kwargs):
        raise NotImplementedError


class Pid(object):

    def __init__(*args, **kwargs):
        raise NotImplementedError


def spawn_async(*args, **kwargs):
    raise NotImplementedError


def add_emission_hook(*args, **kwargs):
    raise NotImplementedError


def signal_new(*args, **kwargs):
    raise NotImplementedError
