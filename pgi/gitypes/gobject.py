# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from glib import *
from ctypes import *
from _util import load, wrap_class

_gobject = load("gobject-2.0")


class GParamFlags(Enum):
    READABLE = 1 << 0
    WRITABLE = 1 << 1
    CONSTRUCT = 1 << 2
    CONSTRUCT_ONLY = 1 << 3
    LAX_VALIDATION = 1 << 4
    STATIC_NAME = 1 << 5
    STATIC_NICK = 1 << 6
    STATIC_BLURB = 1 << 7
    DEPRECATED = 1 << 31


class GSignalFlags(Enum):
    RUN_FIRST = 1 << 0
    RUN_LAST = 1 << 1
    RUN_CLEANUP = 1 << 2
    NO_RECURSE = 1 << 3
    DETAILED = 1 << 4
    ACTION = 1 << 5
    NO_HOOKS = 1 << 6
    MUST_COLLECT = 1 << 7

g_type_init = _gobject.g_type_init
g_type_init.argtypes = []
g_type_init.resttype = None

class GType(guint):
    pass

    def __repr__(self):
        return repr(self.value)

_methods = [
    ("type_name", gchar_p, [GType]),
]

wrap_class(_gobject, GType, None, "g_", _methods)

newv = _gobject.g_object_newv
newv.argtypes = [GType, guint]
newv.resttype = gpointer

free = _gobject.g_free
free.argtypes = [gpointer]
free.resttype = None

# GValue

class GValue(Structure):
    pass


class GValuePtr(POINTER(GValue)):
    _type_ = GValue

GValueTransform = CFUNCTYPE(None, GValuePtr, GValuePtr)

_methods = [
    ("init", GValuePtr, [GValuePtr, GType]),
    ("copy", None, [GValuePtr, GValuePtr]),
    ("reset", GValuePtr, [GValuePtr]),
    ("unset", None, [GValuePtr]),
    ("set_instance", None, [GValuePtr, gpointer]),
    ("fits_pointer", gboolean, [GValuePtr]),
    ("peek_pointer", gpointer, [GValuePtr]),
    ("type_compatible", gboolean, [GType, GType]),
    ("type_transformable", gboolean, [GType, GType]),
    ("transform", gboolean, [GValuePtr, GValuePtr]),
    ("register_transform_func", None, [GType, GType, GValueTransform]),
]

wrap_class(_gobject, GValue, GValuePtr, "g_value_", _methods)

__all__ = ["GType", "g_type_init", "GParamFlags", "GValue", "GValuePtr",
           "GValueTransform", "GSignalFlags"]
