# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import *
from _util import wrap_class, load

_glib = load("glib-2.0")

gchar_p = c_char_p
guint = c_uint
gpointer = c_void_p
gint32 = c_int32
guint32 = c_uint32
gint = c_int
gquark = guint32
gboolean = c_bool
gint8 = c_int8
guint8 = c_uint8
gint16 = c_int16
guint16 = c_uint16
gint64 = c_int64
guint64 = c_uint64
gfloat = c_float
gdouble = c_double
gshort = c_short
gushort = c_ushort
glong = c_long
gulong = c_ulong
gsize = c_size_t


class Enum(guint):
    def __str__(self):
        for a in (c for c in dir(self) if c.upper() == c):
            if getattr(self, a) == self.value:
                return a
        return "Unkown"

    def __repr__(self):
        return repr(str(self))

    def __int__(self):
        return self.value


class Flags(guint):
    def __str__(self):
        values = []
        for a in (c for c in dir(self) if c.upper() == c):
            if getattr(self, a) & self.value:
                values.append(a)
        return " | ".join(values) or "Unkown"

    def __repr__(self):
        return repr(str(self))

    def __int__(self):
        return self.value

# GError


class GError(Structure):
    _fields_ = [
        ("domain", gquark),
        ("code", gint),
        ("message", gchar_p),
    ]


class GErrorPtr(POINTER(GError)):
    _type_ = GError

_methods = [
    ("free", None, [GErrorPtr]),
]

wrap_class(_glib, GError, GErrorPtr, "g_error_", _methods)


class GErrorException(Exception):
    def __init__(self, message):
        super(GErrorException, self).__init__()
        self.message = message

    def __str__(self):
        return self.message


def check_gerror(gerror_ptr):
    try:
        gerror = gerror_ptr.contents
        raise GErrorException(gerror.message)
    except ValueError:
        return

# GMappedFile


class GMappedFile(Structure):
    pass


class GMappedFilePtr(POINTER(GMappedFile)):
    _type_ = GMappedFile

_methods = [
    ("new", GMappedFilePtr, [gchar_p, gboolean, POINTER(POINTER(GError))]),
    #("new_from_fd", GMappedFilePtr,
    # [gint, gboolean, POINTER(POINTER(GError))]),
    ("ref", GMappedFilePtr, [GMappedFilePtr]),
    ("unref", None, [GMappedFilePtr]),
    ("get_length", gsize, [GMappedFilePtr]),
    ("get_contents", gchar_p, [GMappedFilePtr]),
]

wrap_class(_glib, GMappedFile, GMappedFilePtr, "g_mapped_file_", _methods)

# GOptionGroup


class GOptionGroup(Structure):
    pass


class GOptionGroupPtr(POINTER(GOptionGroup)):
    _type_ = GOptionGroup

# GSList


class GSList(Structure):
    pass


class GSListPtr(POINTER(GSList)):
    _type_ = GSList

    def next(self):
        return self.contents.next

GSList._fields_ = [
    ("data", gpointer),
    ("next", GSListPtr),
]

_methods = [
    ("alloc", GSListPtr, []),
    ("append", GSListPtr, [GSListPtr, gpointer]),
    ("prepend", GSListPtr, [GSListPtr, gpointer]),
    ("insert", GSListPtr, [GSListPtr, gpointer, gint]),
    ("insert_before", GSListPtr, [GSListPtr, GSListPtr, gpointer]),
    #("insert_sorted",,[]),
    ("remove", GSListPtr, [GSListPtr, gpointer]),
    ("remove_link", GSListPtr, [GSListPtr, GSListPtr]),
    ("delete_link", GSListPtr, [GSListPtr, GSListPtr]),
    ("remove_all", GSListPtr, [GSListPtr, gpointer]),
    ("free", None, [GSListPtr]),
    #("free_full", None, [GSListPtr, ]),
    ("free_1", None, [GSListPtr]),
    ("length", guint, [GSListPtr]),
    ("copy", GSListPtr, [GSListPtr]),
    ("reverse", GSListPtr, [GSListPtr]),
    #("insert_sorted_with_data", , []),
    #("sort", , []),
    #("sort_with_data", , []),
    ("concat", GSListPtr, [GSListPtr, GSListPtr]),
    #("foreach", , []),
    ("last", GSListPtr, [GSListPtr]),
    ("nth", GSListPtr, [GSListPtr, guint]),
    ("nth_data", gpointer, [GSListPtr, guint]),
    ("find", GSListPtr, [GSListPtr, gpointer]),
    #("find_custom", , []),
    ("position", gint, [GSListPtr, GSListPtr]),
    ("index", gint, [GSListPtr, gpointer]),
]

wrap_class(_glib, GSList, GSListPtr, "g_slist_", _methods)

# GList


class GList(Structure):
    pass


class GListPtr(POINTER(GList)):
    _type_ = GList

    def next(self):
        return self.contents.next

    def previous(self):
        return self.contents.previous

GList._fields_ = [
    ("data", gpointer),
    ("next", GListPtr),
    ("prev", GListPtr),
]

_methods = [
    ("alloc", GListPtr, []),
    ("append", GListPtr, [GListPtr, gpointer]),
    ("prepend", GListPtr, [GListPtr, gpointer]),
    ("insert", GListPtr, [GListPtr, gpointer, gint]),
    ("insert_before", GListPtr, [GListPtr, GListPtr, gpointer]),
    #("insert_sorted",,[]),
    ("remove", GListPtr, [GListPtr, gpointer]),
    ("remove_link", GListPtr, [GListPtr, GListPtr]),
    ("delete_link", GListPtr, [GListPtr, GListPtr]),
    ("remove_all", GListPtr, [GListPtr, gpointer]),
    ("free", None, [GListPtr]),
    #("free_full", None, [GListPtr, ]),
    ("free_1", None, [GListPtr]),
    ("length", guint, [GListPtr]),
    ("copy", GListPtr, [GListPtr]),
    ("reverse", GListPtr, [GListPtr]),
    #("insert_sorted_with_data", , []),
    #("sort", , []),
    #("sort_with_data", , []),
    ("concat", GListPtr, [GListPtr, GListPtr]),
    #("foreach", , []),
    ("first", GListPtr, [GListPtr]),
    ("last", GListPtr, [GListPtr]),
    ("nth", GListPtr, [GListPtr, guint]),
    ("nth_data", gpointer, [GListPtr, guint]),
    ("find", GListPtr, [GListPtr, gpointer]),
    #("find_custom", , []),
    ("position", gint, [GListPtr, GListPtr]),
    ("index", gint, [GListPtr, gpointer]),
]

wrap_class(_glib, GList, GListPtr, "g_list_", _methods)

__all__ = ["gchar_p", "guint", "gpointer", "gint32", "guint32", "gint",
           "gquark", "gboolean", "gint8", "guint8", "gint16", "guint16",
           "gint64", "guint64", "gfloat", "gdouble", "gshort", "gushort",
           "glong", "gulong", "gsize", "Enum", "Flags",
           "GError", "GErrorException", "check_gerror", "GErrorPtr",
           "GMappedFile", "GMappedFilePtr",
           "GOptionGroup", "GOptionGroupPtr",
           "GSList", "GSListPtr",
           "GList", "GListPtr"]
