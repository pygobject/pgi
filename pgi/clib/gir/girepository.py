# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER, c_char_p, c_void_p

from ..glib import guint, gchar_p, GErrorPtr, gboolean, gint
from ..glib import GSListPtr, GOptionGroupPtr, GListPtr
from ..gobject import GType
from .gibaseinfo import GIBaseInfo
from .gitypelib import GITypelib
from ..ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


class GIRepositoryError(guint):
    TYPELIB_NOT_FOUND = 0
    NAMESPACE_MISMATCH = 1
    NAMESPACE_VERSION_CONFLICT = 2
    LIBRARY_NOT_FOUND = 3


class GIRepositoryLoadFlags(guint):
    LAZY = 1


class GIRepository(c_void_p):

    def get_infos(self, namespace):
        n_infos = self.get_n_infos(namespace)
        return [self.get_info(namespace, i) for i in xrange(n_infos)]

    def get_info(self, *args):
        res = self._get_info(*args)
        return GIBaseInfo._cast(res)

    def find_by_gtype(self, *args):
        res = self._find_by_gtype(*args)
        if not res:
            return None
        return GIBaseInfo._cast(res)

    def find_by_name(self, *args):
        res = self._find_by_name(*args)
        if not res:
            return None
        return GIBaseInfo._cast(res)

_methods = [
    ("get_default", GIRepository, []),
    ("require", GITypelib, [GIRepository, gchar_p, gchar_p,
                            GIRepositoryLoadFlags,
                            POINTER(GErrorPtr)]),
    ("_find_by_name", GIBaseInfo,
     [GIRepository, gchar_p, gchar_p], True),
    ("get_version", gchar_p, [GIRepository, gchar_p]),
    ("prepend_search_path", None, [c_char_p]),
    ("get_search_path", GSListPtr, []),
    ("load_typelib", c_char_p,
        [GIRepository, GITypelib, GIRepositoryLoadFlags,
         POINTER(GErrorPtr)]),
    ("is_registered", gboolean, [GIRepository, gchar_p, gchar_p]),
    ("require_private",
        GITypelib, [GIRepository, gchar_p, gchar_p, gchar_p,
                    GIRepositoryLoadFlags, POINTER(GErrorPtr)]),
    ("get_dependencies", POINTER(gchar_p), [GIRepository, gchar_p]),
    ("get_loaded_namespaces", POINTER(gchar_p), [GIRepository]),
    ("_find_by_gtype", GIBaseInfo, [GIRepository, GType], True),
    ("get_n_infos", gint, [GIRepository, gchar_p]),
    ("_get_info", GIBaseInfo, [GIRepository, gchar_p, gint], True),
    ("get_typelib_path", gchar_p, [GIRepository, gchar_p]),
    ("get_shared_library", gchar_p, [GIRepository, gchar_p]),
    ("get_version", gchar_p, [GIRepository, gchar_p]),
    ("get_option_group", GOptionGroupPtr, [], True),
    ("get_c_prefix", gchar_p, [GIRepository, gchar_p]),
    ("dump", gboolean, [c_char_p, POINTER(GErrorPtr)]),
    ("enumerate_versions", GListPtr, [GIRepository, gchar_p]),
]

wrap_class(_gir, None, GIRepository, "g_irepository_", _methods)


__all__ = ["GIRepositoryLoadFlags", "GIRepository", "GIRepositoryError"]
