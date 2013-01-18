# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from cffi import FFI

from pgi.gir import GIRepositoryPtr, GITypeTag
from pgi.codegen.backend import CodeGenBackend
from pgi.codegen.utils import CodeBlock


_glib_defs = """
typedef char gchar;
typedef const void * gconstpointer;
typedef double gdouble;
typedef float gfloat;
typedef int gboolean;
typedef int16_t gint16;
typedef int32_t gint32;
typedef int64_t gint64;
typedef int8_t gint8;
typedef int gint;
typedef long glong;
typedef short gshort;
typedef size_t gsize;
typedef uint16_t guint16;
typedef uint32_t guint32;
typedef uint64_t guint64;
typedef uint8_t guint8;
typedef unsigned int guint;
typedef unsigned long gulong;
typedef unsigned short gushort;
typedef void* gpointer;"""


def typeinfo_to_cffi(info):
    tag = info.tag.value
    ptr = info.is_pointer

    if not ptr:
        if tag == GITypeTag.UINT32:
            return "guint32"
        elif tag == GITypeTag.BOOLEAN:
            return "gboolean"
    else:
        if tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return "gchar*"

    raise NotImplementedError


class BasicTypes(object):

    def unpack_string(self, name):
        to_string = self.var()
        block, var = self.parse("""
$string = $to_string($cdata)
""", to_string=to_string, cdata=name)

        block.add_dependency(to_string, self._ffi.string)
        return block, var["string"]

    def unpack_bool(self, name):
        block, var = self.parse("""
$bool = bool($name)
""", name=name)

        return block, var["bool"]


class CFFIBackend(CodeGenBackend, BasicTypes):

    NAME = "cffi"

    def __init__(self, *args, **kwargs):
        CodeGenBackend.__init__(self, *args, **kwargs)
        self._libs = {}
        try:
            self._ffi = FFI()
        except ImportError:
            raise NotImplementedError
        else:
            self._ffi.cdef(_glib_defs)

    def get_library_object(self, namespace):
        if namespace not in self._libs:
            paths = GIRepositoryPtr().get_shared_library(namespace)
            if not paths:
                return
            path = paths.split(",")[0]
            # pfff, strip so verion
            path = path[3:].rsplit(".", 1)[0]
            self._libs[namespace] = self._ffi.dlopen(path)
        return self._libs[namespace]

    def get_function_object(self, lib, symbol, args, ret,
                            method=False, self_name="", throws=False):
        if args:
            raise NotImplementedError

        block = CodeBlock()
        cdef_types = []

        if method:
            cdef_types.append("gpointer")
            self_block, var = self.parse("""
$new_self = ffi.cast('gpointer', $sself._obj)
""", sself=self_name)
            block.add_dependency("ffi", self._ffi)
            self_block.write_into(block)

        if ret:
            cffi_ret = typeinfo_to_cffi(ret.type)
        else:
            cffi_ret = "void"

        cdef = "%s %s(%s);" % (cffi_ret, symbol, ", ".join(cdef_types))
        self._ffi.cdef(cdef, override=True)
        block.write_line("# " + cdef)

        return block, method and var["new_self"], getattr(lib, symbol)

    def call(self, name, args):
        block, var = self.parse("""
# call '$name'
$ret = $name($args)
""", name=name, args=args)

        return block, var["ret"]
