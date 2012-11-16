# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import Structure, POINTER, c_char_p

from pgi.glib import guint, gchar_p, GError, gboolean, gint
from pgi.glib import GSListPtr, GOptionGroupPtr, GListPtr
from pgi.gobject import GType
from gibaseinfo import GIBaseInfoPtr
from gitypelib import GITypelibPtr
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


class GIRepositoryError(guint):
    (TYPELIB_NOT_FOUND, NAMESPACE_MISMATCH,
     NAMESPACE_VERSION_CONFLICT, LIBRARY_NOT_FOUND) = range(4)


class GIRepositoryLoadFlags(guint):
    LAZY = 1


class GIRepository(Structure):
    _fields_ = []


class GIRepositoryPtr(POINTER(GIRepository)):
    _type_ = GIRepository

_methods = [
    ("get_default", GIRepositoryPtr, []),
    ("require", GITypelibPtr, [GIRepositoryPtr, gchar_p, gchar_p,
                               GIRepositoryLoadFlags,
                               POINTER(POINTER(GError))]),
    ("find_by_name", GIBaseInfoPtr, [GIRepositoryPtr, gchar_p, gchar_p]),
    ("get_version", gchar_p, [GIRepositoryPtr, gchar_p]),
    ("prepend_search_path", None, [c_char_p]),
    ("get_search_path", GSListPtr, []),
    ("load_typelib", c_char_p,
        [GIRepositoryPtr, GITypelibPtr, GIRepositoryLoadFlags,
         POINTER(POINTER(GError))]),
    ("is_registered", gboolean, [GIRepositoryPtr, gchar_p, gchar_p]),
    ("require_private",
        GITypelibPtr, [GIRepositoryPtr, gchar_p, gchar_p, gchar_p,
                       GIRepositoryLoadFlags, POINTER(POINTER(GError))]),
    ("get_dependencies", POINTER(gchar_p), [GIRepositoryPtr, gchar_p]),
    ("get_loaded_namespaces", POINTER(gchar_p), [GIRepositoryPtr]),
    ("find_by_gtype", GIBaseInfoPtr, [GIRepositoryPtr, GType]),
    ("get_n_infos", gint, [GIRepositoryPtr, gchar_p]),
    ("get_info", GIBaseInfoPtr, [GIRepositoryPtr, gchar_p, gint]),
    ("get_typelib_path", gchar_p, [GIRepositoryPtr, gchar_p]),
    ("get_shared_library", gchar_p, [GIRepositoryPtr, gchar_p]),
    ("get_version", gchar_p, [GIRepositoryPtr, gchar_p]),
    ("get_option_group", GOptionGroupPtr, []),
    ("get_c_prefix", gchar_p, [GIRepositoryPtr, gchar_p]),
    ("dump", gboolean, [c_char_p, POINTER(POINTER(GError))]),
    ("enumerate_versions", GListPtr, [GIRepositoryPtr, gchar_p]),
]

wrap_class(_gir, GIRepository, GIRepositoryPtr, "g_irepository_", _methods)

__all__ = ["GIRepositoryLoadFlags", "GIRepository", "GIRepositoryPtr",
           "GIRepositoryError"]
