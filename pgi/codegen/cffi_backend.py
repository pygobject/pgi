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
typedef void* gpointer;
typedef gulong GType;
"""


def typeinfo_to_cffi(info):
    tag = info.tag.value
    ptr = info.is_pointer

    if not ptr:
        if tag == GITypeTag.UINT32:
            return "guint32"
        elif tag == GITypeTag.INT32:
            return "gint32"
        elif tag == GITypeTag.BOOLEAN:
            return "gboolean"
        elif tag == GITypeTag.VOID:
            return "void"
        elif tag == GITypeTag.GTYPE:
            return "GType"
        elif tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            if iface_type == GIInfoType.STRUCT:
                return "gpointer"
            elif iface_type == GIInfoType.ENUM:
                return "guint32"

            raise NotImplementedError(
                "Couldn't convert interface ptr %r to cffi type" % iface.type)
    else:
        if tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return "gchar*"
        elif tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            if iface_type == GIInfoType.ENUM:
                return "guint32"
            elif iface_type == GIInfoType.OBJECT:
                return "gpointer"
            elif iface_type == GIInfoType.STRUCT:
                return "gpointer"

            raise NotImplementedError(
                "Couldn't convert interface %r to cffi type" % iface.type)

    raise NotImplementedError("Couldn't convert %r to cffi type" % info.tag)


class BasicTypes(object):

    def unpack_utf8(self, name):
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

    def unpack_basic(self, name):
        block, var = self.parse("""
$value = int($value)
""", value=name)

        return block, name

    def pack_bool(self, name):
        block, var = self.parse("""
$boolean = bool($var)
""", var=name)

        return block, var["boolean"]

    def pack_utf8(self, name):
        block, var = self.parse("""
# pack string, no None
if isinstance($var, unicode):
    $var = $var.encode("utf-8")
elif not isinstance($var, str):
    raise TypeError("$var must be a string")
""", var=name)

        return block, name

    def pack_utf8_null(self, name):
        block, var = self.parse("""
# pack string, allow None
if $var is not None:
    if isinstance($var, unicode):
        $var = $var.encode("utf-8")
    elif not isinstance($var, str):
        raise TypeError("$var must be a string or None")
else:
    $var = ffi.cast("char*", 0)
""", var=name)

        return block, name

    def pack_gtype(self, name):
        block, var = self.parse("""
if not isinstance($pgtype, PGType):
    raise TypeError("%r not a GType" % $pgtype)
$gtype = $pgtype._type.value
""", pgtype=name)

        block.add_dependency("PGType", PGType)
        return block, var["gtype"]

    def unpack_gtype(self, name):
        block, var = self.parse("""
$pgtype = PGType($gtype)
""", gtype=name)

        block.add_dependency("PGType", PGType)
        return block, var["pgtype"]


class InterfaceTypes(object):

    def pack_struct(self, name):
        from pgi.util import import_attribute
        base_obj = import_attribute("GObject", "Object")
        from pgi.structure import BaseStructure

        block, var = self.parse("""
if not isinstance($obj, ($base_struct_class, $base_obj_class)):
    raise TypeError("%r is not a structure object" % $obj)
$obj = ffi.cast("void*", $obj._obj)
""", obj=name, base_struct_class=BaseStructure, base_obj_class=base_obj)

        block.add_dependency("ffi", self._ffi)
        return block, var["obj"]

    def pack_object_null(self, obj_name):
        from pgi.util import import_attribute
        gobj_class = import_attribute("GObject", "Object")

        block, var = self.parse("""
if $obj is not None:
    if not isinstance($obj, $gobject):
        raise TypeError("%r not a GObject.Object or None" % $obj)
    $obj = ffi.cast("void*", $obj._obj)
else:
    $obj = ffi.cast("void*", 0)
""", obj=obj_name, gobject=gobj_class)

        block.add_dependency("ffi", self._ffi)
        return block, var["obj"]

    def unpack_object(self, name):
        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = G_TYPE_FROM_INSTANCE(instance.contents)
            return PGType(gtype).pytype

        block, var = self.parse("""
# unpack object
$address = int(ffi.cast("size_t", $value))
if $address:
    $pyclass = $get_class($address)
    $obj = object.__new__($pyclass)
    $obj._obj = $address
else:
    $obj = None
""", value=name, get_class=get_class_func)

        block.add_dependency("ffi", self._ffi)
        return block, var["obj"]

    def setup_struct(self, name, type_):
        block, var = self.parse("""
# setup struct
$obj = $type()
$obj._needs_free = False
$ptr = ffi.cast("void*", $obj._obj)
""", value=name, type=type_)

        block.add_dependency("ffi", self._ffi)
        return block, var["obj"], var["ptr"]


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

    def call(self, func, args):
        block, var = self.parse("""
$ret = $name($args)
""", name=func, args=args)

        return block, var["ret"]

    def cast_pointer(self, name, type_):
        block, var = self.parse("""
$value = ffi.cast("$type*", $value)
""", value=name, type=typeinfo_to_cffi(type_))

        block.add_dependency("ffi", self._ffi)
        return block, name

    def deref_pointer(self, name):
        block, var = self.parse("""
$value = $value[0]
""", value=name)

        return block, var["value"]
