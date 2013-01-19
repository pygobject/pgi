# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes
from cffi import FFI

from pgi.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr
from pgi.gir import GIRepositoryPtr, GITypeTag, GIInfoType
from pgi.gtype import PGType
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
        elif tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            iface.unref()
            if iface_type == GIInfoType.ENUM:
                return "guint32"
            elif iface_type == GIInfoType.OBJECT:
                return "gpointer"

    raise NotImplementedError("Couldn't convert %r to cffi type" % info.tag)


class BasicTypes(object):

    def unpack_string(self, name):
        # most annotations don't specify if the return value for gchar*
        # can be NULL... so check for all strings
        block, var = self.parse("""
if $cdata != ffi.NULL:
    $string = ffi.string($cdata)
else:
    $string = None
""", cdata=name)

        block.add_dependency("ffi", self._ffi)
        return block, var["string"]

    def unpack_bool(self, name):
        block, var = self.parse("""
$bool = bool($name)
""", name=name)

        return block, var["bool"]

    def pack_uint32(self, name):
        block, var = self.parse("""
if not isinstance($uint, (float, int, long)):
    raise TypeError("Value '$uint' not a number")
$uint = int($uint)
# overflow check for uint32
if not 0 <= $uint < 4294967296:
    raise ValueError("Value '$uint' not in range")
""", uint=name)

        return block, var["uint"]


class InterfaceTypes(object):

    def unpack_object(self, name):
        get_class = self.var()

        block, var = self.parse("""
# unpack object
$address = int(ffi.cast("size_t", $value))
if $address:
    $pyclass = $get_class($address)
    $obj = object.__new__($pyclass)
    $obj._obj = $address
else:
    $obj = None
""", value=name, get_class=get_class)


        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = G_TYPE_FROM_INSTANCE(instance.contents)
            return PGType(gtype).pytype

        block.add_dependency(get_class, get_class_func)
        block.add_dependency("ffi", self._ffi)
        return block, var["obj"]

class CFFIBackend(CodeGenBackend, BasicTypes, InterfaceTypes):

    NAME = "cffi"

    def __init__(self, *args, **kwargs):
        CodeGenBackend.__init__(self, *args, **kwargs)
        self._libs = {}
        self._ffi = None

    def __init_ffi(self):
        if self._ffi is None:
            self._ffi = FFI()
            self._ffi.cdef(_glib_defs)

    def get_library_object(self, namespace):
        self.__init_ffi()
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

        block = CodeBlock()
        cdef_types = []

        if method:
            cdef_types.append("gpointer")
            self_block, var = self.parse("""
$new_self = ffi.cast('gpointer', $sself._obj)
""", sself=self_name)
            block.add_dependency("ffi", self._ffi)
            self_block.write_into(block)

        for arg in args:
            cdef_types.append(typeinfo_to_cffi(arg.type))

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
