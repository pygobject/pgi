# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from cffi import FFI

from pgi.clib.gir import GIRepositoryPtr, GITypeTag, GIInfoType
from .backend import Backend, VariableFactory
from .utils import CodeBlock, parse_with_objects


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
typedef intptr_t gpointer;
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


def get_type(type_, gen, may_be_null, may_return_null):
    tag_value = type_.tag.value
    for obj in globals().values():
        if isinstance(obj, type) and issubclass(obj, BaseType):
            if obj.GI_TYPE_TAG == tag_value:
                cls = obj
                break
    else:
        raise NotImplementedError("type: %r", type_.tag)

    cls = cls.get_class(type_)
    return cls(gen, type_, may_be_null, may_return_null)


class BaseType(object):
    GI_TYPE_TAG = None
    type = None
    py_type = None

    def __init__(self, gen, type_, may_be_null, may_return_null):
        self._gen = gen
        self.block = CodeBlock()
        self.type = type_
        self.may_be_null = may_be_null
        self.may_return_null = may_return_null

    def get_type(self, type_, may_be_null=False, may_return_null=False):
        return get_type(type_, self._gen, may_be_null, may_return_null)

    def var(self):
        return self._gen.var()

    @classmethod
    def get_class(cls, type_):
        return cls

    def parse(self, code, **kwargs):
        block, var = self._gen.parse(code, **kwargs)
        block.write_into(self.block)
        return var

    def pre_unpack(self, name):
        return name

    def get_reference(self, value):
        raise NotImplementedError

    def free(self, name):
        raise NotImplementedError


class BasicType(BaseType):

    def pack_in(self, name):
        return name


class Boolean(BasicType):
    GI_TYPE_TAG = GITypeTag.BOOLEAN

    def check(self, name):
        return self.parse("""
$bool = bool($value)
""", value=name)["bool"]

    def pack(self, name):
        return name

    def unpack(self, name):
        return self.parse("""
$bool = bool($value)
""", value=name)["bool"]

    def new(self):
        return self.parse("""
$value = ffi.cast("gboolean", 0)
""")["value"]


class Int32(BasicType):
    GI_TYPE_TAG = GITypeTag.INT32

    def check(self, name):
        return self.parse("""
# int32 type/value check
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

if not -2**31 <= $int < 2**31:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to cffi
$c_value = ffi.cast("gint32", $value)
""", value=valid)["c_value"]

    def unpack(self, name):
        raise NotImplementedError

    def new(self):
        return self.parse("""
# new int32
$value = ffi.cast("gint32", 0)
""")["value"]


class Utf8(BasicType):
    GI_TYPE_TAG = GITypeTag.UTF8

    def check(self, name):
        if self.may_be_null:
            return self.parse("""
if $value is not None:
    if isinstance($value, unicode):
        $string = $value.encode("utf-8")
    elif not isinstance($value, str):
        raise TypeError("%r not a string or None" % $value)
    else:
        $string = $value
else:
    $string = None
""", value=name)["string"]

        return self.parse("""
if isinstance($value, unicode):
    $string = $value.encode("utf-8")
elif not isinstance($value, str):
    raise TypeError("%r not a string" % $value)
else:
    $string = $value
""", value=name)["string"]

    def pack(self, name):
        return self.parse("""
if $value:
    $c_value = $value
else:
    $c_value = ffi.cast("char*", 0)
""", value=name)["c_value"]

    def dup(self, name):
        raise NotImplementedError

    def unpack(self, name):
        raise NotImplementedError

    def unpack_return(self, name):
        raise NotImplementedError

    def new(self):
        raise NotImplementedError


class CFFICodeGen(object):
    def __init__(self, var, ffi):
        self.var = var
        self._ffi = ffi

    def parse(self, code, **kwargs):
        block, var = parse_with_objects(code, self.var, **kwargs)
        block.add_dependency("ffi", self._ffi)
        return block, var


class CFFIBackend(Backend):
    NAME = "cffi"

    _libs = {}
    _ffi = FFI()
    _ffi.cdef(_glib_defs)

    def __init__(self):
        Backend.__init__(self)
        self._gen = CFFICodeGen(VariableFactory(), self._ffi)

    def get_library(self, namespace):
        if namespace not in self._libs:
            paths = GIRepositoryPtr().get_shared_library(namespace)
            if not paths:
                raise NotImplementedError("No shared library")
            path = paths.split(",")[0]
            self._libs[namespace] = self._ffi.dlopen(path)
        return self._libs[namespace]

    def get_function(self, lib, symbol, args, ret,
                     method=False, self_name="", throws=False):

        block = CodeBlock()
        cdef_types = []

        if method:
            cdef_types.append("gpointer")
            self_block, var = self.parse("""
$new_self = $sself._obj
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

        try:
            func = getattr(lib, symbol)
        except (KeyError, AttributeError):
            raise NotImplementedError(
                "Library doesn't provide symbol: %s" % symbol)

        return block, method and var["new_self"], func

    def get_type(self, type_, may_be_null=False, may_return_null=False):
        return get_type(type_, self._gen, may_be_null, may_return_null)

    def parse(self, code, **kwargs):
        return self._gen.parse(code, **kwargs)

    def cast_pointer(self, name, type_):
        block, var = self.parse("""
$value = ffi.cast("$type*", $value)
""", value=name, type=typeinfo_to_cffi(type_))

        block.add_dependency("ffi", self._ffi)
        return block, name

    def assign_pointer(self, ptr, value):
        raise NotImplementedError

    def deref_pointer(self, name):
        block, var = self.parse("""
$value = $value[0]
""", value=name)

        return block, var["value"]
