# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .. import glib
from .. import _create_enum_class, _unpack_zeroterm_char_array

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
        return glib.GSList(lib.g_irepository_get_search_path())

    def is_registered(self, namespace, version):
        return bool(lib.g_irepository_is_registered(self._ptr,
                                                    namespace, version))

    def find_by_name(self, namespace, name):
        res = lib.g_irepository_find_by_name(self._ptr, namespace, name)
        if res == ffi.NULL:
            return
        type_ = GIBaseInfo._get_type(res)
        return type_(res)

    def require(self, namespace, version, flags):
        if version is None:
            version = ffi.cast("gchar*", ffi.NULL)
        with glib.gerror(GIError) as error:
            res = lib.g_irepository_require(self._ptr, namespace, version,
                                            flags, error)
        return GITypelib(res)

    def require_private(self, typelib_dir, namespace, version, flags):
        if version is None:
            version = ffi.cast("gchar*", ffi.NULL)
        with glib.gerror() as error:
            res = lib.g_irepository_require_private(self._ptr, typelib_dir,
                                                    namespace, version,
                                                    flags, error)
        return GITypelib(res)

    def get_dependencies(self, namespace):
        res = lib.g_irepository_get_dependencies(self._ptr, namespace)
        return _unpack_zeroterm_char_array(ffi, res)

    def get_loaded_namespaces(self):
        res = lib.g_irepository_get_loaded_namespaces(self._ptr)
        res = _unpack_zeroterm_char_array(ffi, res)
        return res

    def find_by_gtype(self, gtype):
        res = lib.g_irepository_find_by_gtype(self._ptr, gtype)
        if res:
            type_ = GIBaseInfo._get_type(res)
            return type_(res)

    def get_n_infos(self, namespace):
        return lib.g_irepository_get_n_infos(self._ptr, namespace)

    def get_info(self, namespace, index):
        res = lib.g_irepository_get_info(self._ptr, namespace, index)
        type_ = GIBaseInfo._get_type(res)
        return type_(res)

    def get_typelib_path(self, namespace):
        res = lib.g_irepository_get_typelib_path(self._ptr, namespace)
        if res:
            return ffi.string(res)

    def get_shared_library(self, namespace):
        res = lib.g_irepository_get_shared_library(self._ptr, namespace)
        if res:
            return ffi.string(res)

    def get_version(self, namespace):
        return ffi.string(lib.g_irepository_get_version(self._ptr, namespace))

    def get_c_prefix(self, namespace):
        res = lib.g_irepository_get_c_prefix(self._ptr, namespace)
        if res:
            return ffi.string(res)

    def dump(self, arg):
        with glib.gerror(GIError) as error:
            res = lib.g_irepository_dump(arg, error)
        return bool(res)

    def enumerate_versions(self, namespace):
        res = lib.g_irepository_enumerate_versions(self._ptr, namespace)
        l = glib.GList(res)
        return [ffi.string(e) for e in l._unpack("gchar*")]
