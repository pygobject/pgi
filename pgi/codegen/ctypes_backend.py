# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.codegen.backend import CodeGenBackend
from pgi.gir import GIRepositoryPtr, GITypeTag, GIInfoType
from pgi.glib import *
from pgi.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr, GType
from pgi.gobject import GCallback
from pgi.gtype import PGType


def typeinfo_to_ctypes(info, return_value=False):

    tag = info.tag.value
    ptr = info.is_pointer

    mapping = {
        GITypeTag.BOOLEAN: gboolean,
        GITypeTag.INT8: gint8,
        GITypeTag.UINT8: guint8,
        GITypeTag.INT16: gint16,
        GITypeTag.UINT16: guint16,
        GITypeTag.INT32: gint32,
        GITypeTag.UINT32: guint32,
        GITypeTag.INT64: gint64,
        GITypeTag.UINT64: guint64,
        GITypeTag.FLOAT: gfloat,
        GITypeTag.DOUBLE: gdouble,
        GITypeTag.VOID: None,
        GITypeTag.GTYPE: GType,
    }

    if ptr:
        if tag == GITypeTag.INTERFACE:
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
        else:
            if tag in mapping:
                return ctypes.POINTER(mapping[tag])
    else:
        if tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            iface.unref()
            if iface_type == GIInfoType.ENUM:
                return guint32
            elif iface_type == GIInfoType.OBJECT:
                return gpointer
            elif iface_type == GIInfoType.STRUCT:
                return gpointer
            elif iface_type == GIInfoType.UNION:
                return gpointer
            elif iface_type == GIInfoType.FLAGS:
                return gint
            raise NotImplementedError(
                "Could not convert interface: %r to ctypes type" % iface.type)
        else:
            if tag in mapping:
                return mapping[tag]

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
$var = bool($var)
$boolean = ctypes.c_bool($var)
""", var=name)

        block.add_dependency("ctypes", ctypes)
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
if isinstance($uint, str):
    try:
        $uint = ord($uint)
    except TypeError:
        raise TypeError("'$uint' must be a single character")

try:
    $uint = int($uint)
except (ValueError, TypeError):
    raise TypeError("Value '$uint' not a number or character")

# pack uint8
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
if isinstance($float, basestring):
    raise TypeError
$float = float($float)
$c_float = ctypes.c_float($float)
if $c_float.value != $float:
    try:
        # easy check for nan/inf
        $c_float.value.as_integer_ratio()
    except:
        raise ValueError("$float(%f) out of range" % $float)
""", float=name)

        return block, var["c_float"]

    def pack_double(self, name):
        block, var = self.parse("""
# pack double
if isinstance($double, basestring):
    raise TypeError
$double = float($double)
$c_double = ctypes.c_double($double)
if $c_double.value != $double:
    try:
        # easy check for nan/inf
        $c_double.value.as_integer_ratio()
    except:
        raise ValueError("$double(%f) out of range" % $double)
""", double=name)

        return block, var["c_double"]

    def pack_uint16(self, name):
        block, var = self.parse("""
# pack uint16
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for uint16
if not 0 <= $value < 2**16:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_uint16($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_int8(self, name):
        block, var = self.parse("""
# pack int8
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for int8
if not -2**7 <= $value < 2**7:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int8($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_int16(self, name):
        block, var = self.parse("""
# pack int16
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for int16
if not -2**15 <= $value < 2**15:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int16($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_int32(self, name):
        block, var = self.parse("""
# pack int32
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for int32
if not -2**31 <= $value < 2**31:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int32($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_int64(self, name):
        block, var = self.parse("""
# pack int64
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for int64
if not -2**63 <= $value < 2**63:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int64($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_uint32(self, name):
        block, var = self.parse("""
# pack uint32
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value '$value' not a number")

# overflow check for uint32
if not 0 <= $value < 2**32:
    raise ValueError("Value '$value' not in range")
$value = ctypes.c_uint32($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def pack_uint64(self, name):
        block, var = self.parse("""
# pack uint64
if not isinstance($value, (int, long)):
    try:
        $value = $value.__int__()
    except AttributeError:
        raise TypeError("Value %r not a number" % $value)

# overflow check for uint64
if not 0 <= $value < 2**64:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_uint64($value)
""", value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_int64(self):
        block, var = self.parse("""
# new int64
$value = ctypes.c_int64()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_uint64(self):
        block, var = self.parse("""
# new uint64
$value = ctypes.c_uint64()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_uint32(self):
        block, var = self.parse("""
# new uint32
$value = ctypes.c_uint32()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_int32(self):
        block, var = self.parse("""
# new int32
$value = ctypes.c_int32()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_float(self):
        block, var = self.parse("""
# new float
$value = ctypes.c_float()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_bool(self):
        block, var = self.parse("""
# new bool
$value = ctypes.c_bool()
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_uint8(self):
        block, var = self.parse("""
# new uint8
$value = ctypes.c_uint8()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_int8(self):
        block, var = self.parse("""
# new int8
$value = ctypes.c_int8()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_int16(self):
        block, var = self.parse("""
# new int16
$value = ctypes.c_int16()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_uint16(self):
        block, var = self.parse("""
# new uint16
$value = ctypes.c_uint16()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_double(self):
        block, var = self.parse("""
# new double
$value = ctypes.c_double()
""")
        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

    def setup_gtype(self):
        block, var = self.parse("""
$gtype = GType()
""")
        block.add_dependency("GType", GType)
        return block, var["gtype"]

    def unpack_gtype(self, name):
        block, var = self.parse("""
$pgtype = PGType($gtype)
""", gtype=name)

        block.add_dependency("PGType", PGType)
        return block, var["pgtype"]

    def pack_gtype(self, name):
        block, var = self.parse("""
if not isinstance($pgtype, PGType):
    raise TypeError("%r not a GType" % $pgtype)
$gtype = GType($pgtype._type.value)
""", pgtype=name)

        block.add_dependency("PGType", PGType)
        block.add_dependency("GType", GType)
        return block, var["gtype"]


class InterfaceTypes(object):

    def pack_object(self, obj_name):
        from pgi.util import import_attribute
        gobj_class = import_attribute("GObject", "Object")

        block, var = self.parse("""
if not isinstance($obj, $gobject):
    raise TypeError("%r not a GObject.Object" % $obj)
$obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=obj_name, gobject=gobj_class)

        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def pack_object_null(self, obj_name):
        from pgi.util import import_attribute
        gobj_class = import_attribute("GObject", "Object")

        block, var = self.parse("""
if $obj is not None:
    if not isinstance($obj, $gobject):
        raise TypeError("%r not a GObject.Object or None" % $obj)
    $obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=obj_name, gobject=gobj_class)

        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def unpack_object(self, name):
        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = G_TYPE_FROM_INSTANCE(instance.contents)
            return PGType(gtype).pytype

        block, var = self.parse("""
# unpack object
if $value:
    $pyclass = $get_class($value)
    $obj = object.__new__($pyclass)
    $obj._obj = $value
else:
    $obj = $value
""", value=name, get_class=get_class_func)

        return block, var["obj"]

    def setup_struct(self, name, type_):
        block, var = self.parse("""
# setup struct
$obj = $type()
$obj._needs_free = False
$ptr = ctypes.c_void_p($obj._obj)
""", value=name, type=type_)

        block.add_dependency("ctypes", ctypes)
        return block, var["obj"], var["ptr"]

    def unpack_struct(self, name, type_):
        block, var = self.parse("""
# unpack struct
if $value:
    $obj = object.__new__($type)
    $obj._obj = $value
else:
    $obj = None
""", value=name, type=type_)

        return block, var["obj"]

    def pack_struct(self, name):
        from pgi.util import import_attribute
        base_obj = import_attribute("GObject", "Object")
        from pgi.structure import BaseStructure

        block, var = self.parse("""
if not isinstance($obj, ($base_struct_class, $base_obj_class)):
    raise TypeError("%r is not a structure object" % $obj)
$obj = ctypes.cast($obj._obj, ctypes.c_void_p)
""", obj=name, base_struct_class=BaseStructure, base_obj_class=base_obj)

        block.add_dependency("ctypes", ctypes)
        return block, var["obj"]

    def unpack_enum(self, name, type_):
        block, var = self.parse("""
# unpack enum
$enum = $enum_class($value)
""", enum_class=type_, value=name)

        return block, var["enum"]

    def unpack_union(self, name, type_):
        block, var = self.parse("""
# unpack union
$union = object.__new__($union_class)
$union._obj = $value
""", union_class=type_, value=name)

        return block, var["union"]

    def unpack_flags(self, name, type_):
        block, var = self.parse("""
# unpack flags
$flags = $flags_class($value)
""", flags_class=type_, value=name)

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
        block, var = self.parse("""
$ptr = $gerror_ptr()
$ptr_ref = ctypes.byref($ptr)
""", gerror_ptr=GErrorPtr)

        block.add_dependency("ctypes", ctypes)
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
        block, var = self.parse("""
$value = ctypes.cast($value, ctypes.POINTER($type))
""", value=name, type=typeinfo_to_ctypes(type_))

        block.add_dependency("ctypes", ctypes)
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

    def get_reference(self, value):
        block, var = self.parse("""
$ptr = ctypes.byref($value)
""", value=value)

        block.add_dependency("ctypes", ctypes)
        return block, var["ptr"]

    def get_callback_object(self, func, args):
        arg_types = [typeinfo_to_ctypes(a.type) for a in args]
        cb_object_type = ctypes.CFUNCTYPE(None, *arg_types)
        return ctypes.cast(cb_object_type(func), GCallback)
