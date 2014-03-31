# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .. import glib
from ..glib import unpack_zeroterm_array, unpack_glist
from .. import _create_enum_class
from .._utils import fsdecode
from .._compat import PY3

from ._ffi import ffi, lib
from .gibaseinfo import GITypelib, GIBaseInfo
from .error import GIError


GIRepositoryLoadFlags = _create_enum_class(ffi, "GIRepositoryLoadFlags",
                                           "G_IREPOSITORY_LOAD_FLAG_")


class GIRepository(object):
    def __init__(self, ptr=ffi.NULL):
        self._ptr = ptr

    @classmethod
    def get_default(cls):
        return GIRepository(lib.g_irepository_get_default())

    @classmethod
    def prepend_search_path(cls, directory):
        lib.g_irepository_prepend_search_path(directory)

    @classmethod
    def prepend_library_path(cls, directory):
        lib.g_irepository_prepend_library_path(directory)

    @classmethod
    def get_search_path(cls):
        res = lib.g_irepository_get_search_path()
        paths = [ffi.string(p) for p in unpack_glist(res, "gchar*",
                                                     transfer_full=False)]
        return [fsdecode(p) for p in paths]

    def is_registered(self, namespace, version):
        if version is None:
            version = ffi.cast("gchar*", ffi.NULL)
        elif PY3:
            version = version.encode("ascii")
        if PY3:
            namespace = namespace.encode("ascii")
        return bool(lib.g_irepository_is_registered(self._ptr,
                                                    namespace, version))

    def find_by_name(self, namespace, name):
        if PY3:
            namespace = namespace.encode("ascii")
            name = name.encode("ascii")
        res = lib.g_irepository_find_by_name(self._ptr, namespace, name)
        if res == ffi.NULL:
            return
        type_ = GIBaseInfo._get_type(res)
        return type_(res)

    def require(self, namespace, version, flags):
        if version is None:
            version = ffi.cast("gchar*", ffi.NULL)
        elif PY3:
            version = version.encode("ascii")
        if PY3:
            namespace = namespace.encode("ascii")
        with glib.gerror(GIError) as error:
            res = lib.g_irepository_require(self._ptr, namespace, version,
                                            flags, error)
        return GITypelib(res)

    def require_private(self, typelib_dir, namespace, version, flags):
        if version is None:
            version = ffi.cast("gchar*", ffi.NULL)
        elif PY3:
            version = version.encode("ascii")
        if PY3:
            namespace = namespace.encode("ascii")
        with glib.gerror() as error:
            res = lib.g_irepository_require_private(self._ptr, typelib_dir,
                                                    namespace, version,
                                                    flags, error)
        return GITypelib(res)

    def get_dependencies(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_get_dependencies(self._ptr, namespace)
        res = [ffi.string(p) for p in unpack_zeroterm_array(res)]
        if PY3:
            res = [p.decode("ascii") for p in res]
        return res

    def get_loaded_namespaces(self):
        res = lib.g_irepository_get_loaded_namespaces(self._ptr)
        res = [ffi.string(p) for p in unpack_zeroterm_array(res)]
        if PY3:
            res = [p.decode("ascii") for p in res]
        return res

    def find_by_gtype(self, gtype):
        res = lib.g_irepository_find_by_gtype(self._ptr, gtype)
        if res:
            type_ = GIBaseInfo._get_type(res)
            return type_(res)

    def get_n_infos(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        return lib.g_irepository_get_n_infos(self._ptr, namespace)

    def get_info(self, namespace, index):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_get_info(self._ptr, namespace, index)
        type_ = GIBaseInfo._get_type(res)
        return type_(res)

    def get_typelib_path(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_get_typelib_path(self._ptr, namespace)
        if res:
            res = ffi.string(res)
            return fsdecode(res)

    def get_shared_library(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_get_shared_library(self._ptr, namespace)
        if res:
            res = ffi.string(res)
            return fsdecode(res)

    def get_version(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = ffi.string(lib.g_irepository_get_version(self._ptr, namespace))
        if PY3:
            res = res.decode("ascii")
        return res

    def get_c_prefix(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_get_c_prefix(self._ptr, namespace)
        if res:
            res = ffi.string(res)
            if PY3:
                res = res.decode("ascii")
            return res

    def enumerate_versions(self, namespace):
        if PY3:
            namespace = namespace.encode("ascii")
        res = lib.g_irepository_enumerate_versions(self._ptr, namespace)
        res = [ffi.string(p) for p in unpack_glist(res, "gchar*")]
        if PY3:
            res = [p.decode("ascii") for p in res]
        return res
