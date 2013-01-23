# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes
from ctypes import POINTER

from pgi.codegen.backend import CodeGenBackend
from pgi.codegen.utils import CodeBlock
from pgi.gir import GIRepositoryPtr, GITypeTag, GIInfoType
from pgi.glib import gboolean, gfloat, gdouble, gint64, guint64, gint, guint8
from pgi.glib import GErrorPtr, gchar_p, guint32, gint32, gpointer, guint16
from pgi.glib import free, gint8
from pgi.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr, GType
from pgi.gtype import PGType
from pgi.util import import_attribute


def typeinfo_to_ctypes(info, return_value=False):

    tag = info.tag.value
    ptr = info.is_pointer

    if ptr:
        if tag == GITypeTag.VOID:
            return gpointer
        elif tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            if return_value:
                # ctypes does auto conversion to str and gives us no chance
                # to free the pointer if transfer=everything
                return gpointer
            else:
                return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
        elif tag == GITypeTag.INTERFACE:
            return gpointer
        elif tag == GITypeTag.INT32:
            return POINTER(gint32)
        elif tag == GITypeTag.UINT32:
            return POINTER(guint32)
        elif tag == GITypeTag.INT64:
            return POINTER(gint64)
        elif tag == GITypeTag.UINT64:
            return POINTER(guint64)
        elif tag == GITypeTag.FLOAT:
            return POINTER(gfloat)
        elif tag == GITypeTag.VOID:
            return gpointer
    else:
        if tag == GITypeTag.BOOLEAN:
            return gboolean
        elif tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            iface.unref()
            if iface_type == GIInfoType.ENUM:
                return guint32
            elif iface_type == GIInfoType.OBJECT:
                return gpointer
            elif iface_type == GIInfoType.STRUCT:
                return gpointer
            elif iface_type == GIInfoType.FLAGS:
                return gint
            raise NotImplementedError(
                "Could not convert interface: %r to ctypes type" % iface.type)
        elif tag == GITypeTag.UINT32:
            return guint32
        elif tag == GITypeTag.UINT64:
            return guint64
        elif tag == GITypeTag.INT32:
            return gint32
        elif tag == GITypeTag.UINT16:
            return guint16
        elif tag == GITypeTag.UINT8:
            return guint8
        elif tag == GITypeTag.INT8:
            return gint8
        elif tag == GITypeTag.INT64:
            return gint64
        elif tag == GITypeTag.FLOAT:
            return gfloat
        elif tag == GITypeTag.DOUBLE:
            return gdouble
        elif tag == GITypeTag.VOID:
            return
        elif tag == GITypeTag.GTYPE:
            return GType

    raise NotImplementedError("Could not convert %r to ctypes type" % info.tag)


class BasicTypes(object):

    def pack_string(self, name):
        # https://bugs.pypy.org/issue466
        block, var = self.parse("""
# https://bugs.pypy.org/issue466
if not isinstance($var, basestring):
    raise TypeError("$var must be a string")
""", var=name)

        return block, name

    def pack_string_null(self, name):
        # https://bugs.pypy.org/issue466
        block, var = self.parse("""
# https://bugs.pypy.org/issue466
if $var is not None and not isinstance($var, basestring):
    raise TypeError("$var must be a string or None")
""", var=name)

        return block, name

    def pack_pointer(self, name):
        block, var = self.parse("""
if $ptr is None:
    raise TypeError("No None allowed")
""", ptr=name)

        return block, name

    def unpack_string(self, name):
        block, var = self.parse("""
$value = ctypes.cast($value, ctypes.c_char_p).value
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, name


    def unpack_string_and_free(self, name):
        block, var = self.parse("""
$str_value = ctypes.cast($value, ctypes.c_char_p).value
free($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        block.add_dependency("free", free)
        return block, var["str_value"]

    def pack_bool(self, name):
        block, var = self.parse("""
# https://bugs.pypy.org/issue1367
$boolean = bool($var)
""", var=name)

        return block, var["boolean"]

    def unpack_bool(self, name):
        block, var = self.parse("""
# pypy returns int instead of bool
$value = bool($value)
""", value=name)

        return block, name

    def unpack_basic(self, name):
        block, var = self.parse("""
# unpack basic ctypes value
$value = $ctypes_value.value
""", ctypes_value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_uint8(self, name):
        block, var = self.parse("""
# uint8: type checking, conversion
if not isinstance($uint, (float, int, long)):
    try:
        $uint = ord($uint)
    except TypeError:
        if isinstance($uint, basestring):
            raise TypeError("'$uint' must be a single character")
        else:
            raise TypeError("Value '$uint' not a number or character")

# pack uint8
$uint = int($uint)
# overflow check for uint8
if not 0 <= $uint < 2**8:
    raise ValueError("Value '$uint' not in range")
$uint = ctypes.c_uint8($uint)
""", uint=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"]

    def pack_float(self, name):
        block, var = self.parse("""
# pack float
#if not isinstance($float, (float, int, long)):
#    raise TypeError("Value '$float' not a number")
$c_float = ctypes.c_float($float)
if $c_float.value != $float:
    raise ValueError("$float out of range")
""", float=name)

        return block, var["c_float"]

    def pack_uint16(self, name):
        block, var = self.parse("""
# pack uint16
if not isinstance($uint, (float, int, long)):
    raise TypeError("Value '$uint' not a number")
$uint = int($uint)
# overflow check for uint16
if not 0 <= $uint < 2**16:
    raise ValueError("Value '$uint' not in range")
$uint = ctypes.c_uint16($uint)
""", uint=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"]

    def pack_int32(self, name):
        block, var = self.parse("""
# pack int32
if not isinstance($int, (float, int, long)):
    raise TypeError("Value '$int' not a number")
$int = int($int)
# overflow check for int32
if not -2**31 <= $int < 2**31:
    raise ValueError("Value '$int' not in range")
$int = ctypes.c_int32($int)
""", int=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["int"]

    def pack_int64(self, name):
        block, var = self.parse("""
# pack int64
if not isinstance($int, (float, int, long)):
    raise TypeError("Value '$int' not a number")
$int = int($int)
# overflow check for int64
if not -2**63 <= $int < 2**63:
    raise ValueError("Value '$int' not in range")
$int = ctypes.c_int64($int)
""", int=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["int"]

    def pack_uint32(self, name):
        block, var = self.parse("""
# pack uint32
if not isinstance($uint, (float, int, long)):
    raise TypeError("Value '$uint' not a number")
$uint = int($uint)
# overflow check for uint32
if not 0 <= $uint < 2**32:
    raise ValueError("Value '$uint' not in range")
$uint = ctypes.c_uint32($uint)
""", uint=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"]

    def pack_uint64(self, name):
        block, var = self.parse("""
# pack uint64
if not isinstance($uint, (float, int, long)):
    raise TypeError("Value '$uint' not a number")
$uint = int($uint)
# overflow check for uint64
if not 0 <= $uint < 2**64:
    raise ValueError("Value '$uint' not in range")
$uint = ctypes.c_uint64($uint)
""", uint=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"]


    def setup_uint32_ptr(self):
        block, var = self.parse("""
# new uint32
$uint = ctypes.c_uint32()
$uint_ref = ctypes.byref($uint)
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"], var["uint_ref"]

    def setup_float_ptr(self):
        block, var = self.parse("""
# new float
$float = ctypes.c_float()
$float_ref = ctypes.byref($float)
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["float"], var["float_ref"]

    def setup_double_ptr(self):
        block, var = self.parse("""
# new double
$value = ctypes.c_double()
$value_ref = ctypes.byref($value)
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["value"], var["value_ref"]

    def unpack_gtype(self, name):
        block, var = self.parse("""
$pgtype = PGType($gtype)
""", gtype=name)

        block.add_dependency("PGType", PGType)
        return block, var["pgtype"]

    def pack_gtype(self, name):
        block, var = self.parse("""
$gtype = $pgtype._type
""", pgtype=name)

        return block, var["gtype"]


class InterfaceTypes(object):

    def unpack_gvalue(self, name):
        from pgi.util import import_module
        gobj = import_module("GObject")
        gobj_var = self.var()

        block, var = self.parse("""
$type = $value.g_type
if $type == $gobj.TYPE_FLOAT:
    $out = $value.get_float()
elif $type == $gobj.TYPE_DOUBLE:
    $out = $value.get_double()
elif $type == $gobj.TYPE_BOOLEAN:
    $out = $value.get_boolean()
elif $type == $gobj.TYPE_GTYPE:
    $out = $value.get_gtype()
elif $type == $gobj.TYPE_INT:
    $out = $value.get_int()
elif $type == $gobj.TYPE_INT64:
    $out = $value.get_int64()
elif $type == $gobj.TYPE_LONG:
    $out = $value.get_long()
elif $type == $gobj.TYPE_ULONG:
    $out = $value.get_ulong()
elif $type == $gobj.TYPE_OBJECT:
    $out = $value.get_object()
elif $type == $gobj.TYPE_CHAR:
    $out = chr($value.get_schar())
elif $type == $gobj.TYPE_UCHAR:
    $out = chr($value.get_uchar())
elif $type == $gobj.TYPE_UINT:
    $out = $value.get_uint()
elif $type == $gobj.TYPE_STRING:
    $out = $value.get_string()
elif $type == $gobj.TYPE_UINT64:
    $out = $value.get_uint64()
elif $type == $gobj.TYPE_POINTER:
    $out = $value.get_pointer()
else:
    # not implemented, return the gvalue at least
    $out = $type
""", gobj=gobj_var, value=name)

        block.add_dependency(gobj_var, gobj)
        return block, var["out"]

    def pack_object(self, obj_name):
        gobj_class = import_attribute("GObject", "Object")
        gobj_var = self.var()

        block, var = self.parse("""
if not isinstance($obj, $gobject):
    raise TypeError("%r not a GObject.Object" % $obj)
$obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=obj_name, gobject=gobj_var)

        block.add_dependency(gobj_var, gobj_class)
        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def pack_object_null(self, obj_name):
        gobj_class = import_attribute("GObject", "Object")
        gobj_var = self.var()

        block, var = self.parse("""
if $obj is not None:
    if not isinstance($obj, $gobject):
        raise TypeError("%r not a GObject.Object or None" % $obj)
    $obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=obj_name, gobject=gobj_var)

        block.add_dependency(gobj_var, gobj_class)
        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def unpack_object(self, name):
        get_class = self.var()

        block, var = self.parse("""
# unpack object
if $value:
    $pyclass = $get_class($value)
    $obj = object.__new__($pyclass)
    $obj._obj = $value
else:
    $obj = $value
""", value=name, get_class=get_class)

        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = G_TYPE_FROM_INSTANCE(instance.contents)
            return PGType(gtype).pytype

        block.add_dependency(get_class, get_class_func)
        return block, var["obj"]

    def setup_struct(self, name, type_):
        struct_type = self.var()

        block, var = self.parse("""
# setup struct
$obj = $type()
$obj._needs_free = False
$ptr = ctypes.c_void_p($obj._obj)
""", value=name, type=struct_type)

        block.add_dependency("ctypes", ctypes)
        block.add_dependency(struct_type, type_)

        return block, var["obj"], var["ptr"]

    def unpack_struct(self, name, type_):
        struct_type = self.var()

        block, var = self.parse("""
# unpack struct
if $value:
    $obj = object.__new__($type)
    $obj._obj = $value
else:
    $obj = None
""", value=name, type=struct_type)

        block.add_dependency(struct_type, type_)
        return block, var["obj"]


    def pack_struct(self, name):
        base_var = self.var()
        base_obj_var = self.var()

        block, var = self.parse("""
if not isinstance($obj, ($base_struct_class, $base_obj_class)):
    raise TypeError("%r is not a structure object" % $obj)
$obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=name, base_struct_class=base_var, base_obj_class=base_obj_var)

        base_obj = import_attribute("GObject", "Object")
        from pgi.structure import BaseStructure
        block.add_dependency(base_var, BaseStructure)
        block.add_dependency(base_obj_var, base_obj)
        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def unpack_enum(self, name, type_):
        type_var = self.var()

        block, var = self.parse("""
# unpack enum
$enum = $enum_class($value)
""", enum_class=type_var, value=name)

        block.add_dependency(type_var, type_)
        return block, var["enum"]

    def unpack_union(self, name, type_):
        type_var = self.var()

        block, var = self.parse("""
# unpack union
$union = object.__new__($union_class)
$union._obj = $value
""", union_class=type_var, value=name)

        block.add_dependency(type_var, type_)
        return block, var["union"]

    def unpack_flags(self, name, type_):
        type_var = self.var()

        block, var = self.parse("""
# unpack flags
$flags = $flags_class($value)
""", flags_class=type_var, value=name)

        block.add_dependency(type_var, type_)
        return block, var["flags"]


class ArrayTypes(object):
    # FIXME: these all ignore item types

    def unpack_array_zeroterm_c(self, in_name):
        block, var = self.parse("""
# extract a zeroterm ctypes array '$array' into the list '$list'
$list = []
$i = 0
$current = $array and $array[$i]
while $current:
    $list.append($current)
    $i += 1
    $current = $array[$i]
""", array=in_name)

        return block, (var["list"],)

    def pack_array_ptr_fixed_c_in_out(self, name):
        block, var = self.parse("""
# pack c array
$length = len($name)
$length_c = ctypes.c_int($length)
$length_ref = ctypes.byref($length_c)
$array = (ctypes.c_char_p * $length)()
for $i, $item in enumerate($name):
    $array[$i] = $item
$array_ptr = ctypes.pointer($array)
$array_ref = ctypes.byref($array_ptr)
""", name=name)

        block.add_dependency("ctypes", ctypes)

        return (block, var["array_ptr"], var["array_ref"],
                var["length_c"], var["length_ref"])

    def pack_array_ptr_fixed_c_in(self, name):
        block, var = self.parse("""
# pack c array
$length = len($name)
$array = (ctypes.c_char_p * $length)()
for $i, $item in enumerate($name):
    $array[$i] = $item
$array_ref = ctypes.byref($array)
""", name=name)

        block.add_dependency("ctypes", ctypes)

        return block, var["array_ref"], var["length"]

    def unpack_array_ptr_fixed_c(self, array, length):
        block, var = self.parse("""
# unpack fixed array
$out = []
$array = $array.contents
for $i in xrange($length.value):
    $out.append($array[$i])
""", array=array, length=length)

        return block, var["out"]


class ErrorTypes(object):

    def setup_gerror(self):
        gerror_var = self.var()
        block, var = self.parse("""
$ptr = $gerror_ptr()
$ptr_ref = ctypes.byref($ptr)
""", gerror_ptr=gerror_var)

        block.add_dependency("ctypes", ctypes)
        block.add_dependency(gerror_var, GErrorPtr)
        return block, var["ptr"], var["ptr_ref"]

    def check_gerror(self, gerror_ptr):
        block, var = self.parse("""
if $gerror_ptr:
    raise RuntimeError($gerror_ptr.contents.message)
""", gerror_ptr=gerror_ptr)

        return block


class CTypesBackend(CodeGenBackend, BasicTypes, InterfaceTypes, ArrayTypes,
                    ErrorTypes):

    NAME = "ctypes"

    def __init__(self, *args, **kwargs):
        CodeGenBackend.__init__(self, *args, **kwargs)
        self._libs = {}

    def get_library_object(self, namespace):
        if namespace not in self._libs:
            paths = GIRepositoryPtr().get_shared_library(namespace)
            if not paths:
                return
            path = paths.split(",")[0]
            lib = getattr(ctypes.cdll, path)
            self._libs[namespace] = lib
        return self._libs[namespace]

    def get_function_object(self, lib, symbol, args, ret,
                            method=False, self_name="", throws=False):
        h = getattr(lib, symbol)
        if ret:
            h.restype = typeinfo_to_ctypes(ret.type, return_value=True)
        else:
            h.restype = None

        arg_types = []

        if method:
            arg_types.append(ctypes.c_void_p)

        if throws:
            args = args[:-1]

        for arg in args:
            type_ = typeinfo_to_ctypes(arg.type)
            # FIXME: cover all types..
            if not type_:
                continue
            if arg.is_direction_out() and type_ != ctypes.c_void_p:
                type_ = ctypes.POINTER(type_)
            arg_types.append(type_)

        if throws:
            arg_types.append(ctypes.c_void_p)

        h.argtypes = arg_types

        block, var = self.parse("""
# args: $args
# ret: $ret
""", args=repr([n.__name__ for n in h.argtypes]), ret=repr(h.restype))

        if method:
            self_block, var = self.parse("""
$new_self = $sself._obj
""", sself=self_name)
            self_block.write_into(block)

        return block, method and var["new_self"], h

    def call(self, name, args):
        block, var = self.parse("""
# call '$name'
try:
    $ret = $name($args)
except ctypes.ArgumentError, $e:
    raise TypeError($e.message)
""", name=name, args=args)

        block.add_dependency("ctypes", ctypes)
        return block, var["ret"]

    def cast_pointer(self, name, type_):
        type_ = typeinfo_to_ctypes(type_)
        type_var = self.var()
        block, var = self.parse("""
$value = ctypes.cast($value, ctypes.POINTER($type))
""", value=name, type=type_var)

        block.add_dependency("ctypes", ctypes)
        block.add_dependency(type_var, type_)

        return block, name

    def deref_pointer(self, name):
        block, var = self.parse("""
$value = $value.contents
""", value=name)

        return block, var["value"]

    def assign_pointer(self, ptr, value):
        block, var = self.parse("""
$ptr[0] = $value
""", ptr=ptr, value=value)

        return block
