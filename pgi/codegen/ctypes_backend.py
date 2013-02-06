# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.codegen.backend import CodeGenBackend
from pgi.gir import GIRepositoryPtr, GITypeTag, GIInfoType
from pgi import glib
from pgi.glib import *
from pgi.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr, GType
from pgi.gobject import GCallback
from pgi.gtype import PGType
from pgi.gerror import PGError


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
        elif tag == GITypeTag.ERROR:
            return GErrorPtr
        else:
            if tag in mapping:
                return ctypes.POINTER(mapping[tag])
    else:
        if tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            if iface_type == GIInfoType.ENUM:
                return guint32
            elif iface_type == GIInfoType.OBJECT:
                return gpointer
            elif iface_type == GIInfoType.STRUCT:
                return gpointer
            elif iface_type == GIInfoType.UNION:
                return gpointer
            elif iface_type == GIInfoType.FLAGS:
                return guint
            elif iface_type == GIInfoType.CALLBACK:
                return GCallback

            raise NotImplementedError(
                "Could not convert interface: %r to ctypes type" % iface.type)
        else:
            if tag in mapping:
                return mapping[tag]

    raise NotImplementedError("Could not convert %r to ctypes type" % info.tag)


class BasicTypes(object):

    def dup_string(self, name):
        block, var = self.parse("""
$ptr_cpy = ctypes.c_char_p(glib.g_strdup($ptr))
""", ptr=name)

        block.add_dependency("glib", glib)
        return block, var["ptr_cpy"]

    def pack_utf8(self, name):
        block, var = self.parse("""
# https://bugs.pypy.org/issue466
if isinstance($var, unicode):
    $var = $var.encode("utf-8")
elif not isinstance($var, str):
    raise TypeError("$var must be a string")
$var = ctypes.c_char_p($var)
""", var=name)

        return block, name

    def pack_utf8_null(self, name):
        block, var = self.parse("""
if $var is not None:
    # https://bugs.pypy.org/issue466
    if isinstance($var, unicode):
        $var = $var.encode("utf-8")
    elif not isinstance($var, str):
        raise TypeError("$var must be a string or None")
$var = ctypes.c_char_p($var)
""", var=name)

        return block, name

    def pack_pointer(self, name):
        block, var = self.parse("""
if $ptr is None:
    raise TypeError("No None allowed")
$ptr = ctypes.c_void_p($ptr)
""", ptr=name)

        return block, name

    def unpack_utf8_return(self, name):
        block, var = self.parse("""
$str_value = ctypes.c_char_p($value).value
""", value=name)

        return block, var["str_value"], name

    def pack_bool(self, name):
        block, var = self.parse("""
# https://bugs.pypy.org/issue1367
$var = bool($var)
$boolean = ctypes.c_bool($var)
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

        return block, var["value"]

    unpack_utf8 = unpack_basic

    def pack_uint8(self, name):
        block, var = self.parse("""
if isinstance($uint, basestring):
    if isinstance($uint, str):
        try:
            $uint = ord($uint)
        except TypeError:
            raise TypeError("'$uint' must be a single character")
    else:
        raise TypeError("Input must be a str character")

$uint = int($uint)

# pack uint8
# overflow check for uint8
if not 0 <= $uint < 2**8:
    raise ValueError("Value '$uint' not in range")
$uint = ctypes.c_uint8($uint)
""", uint=name)

        return block, var["uint"]

    def pack_float(self, name):
        block, var = self.parse("""
# pack float
if isinstance($float, basestring):
    raise TypeError
$float = float($float)
$c_float = ctypes.c_float($float)
$c_value = $c_float.value
if $c_value != $float and $c_value in (float('inf'), float('-inf'), float('nan')):
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
$c_value = $c_double.value
if $c_value != $double and $c_value in (float('inf'), float('-inf'), float('nan')):
    raise ValueError("$double(%f) out of range" % $double)
""", double=name)

        return block, var["c_double"]

    def pack_uint16(self, name):
        block, var = self.parse("""
# pack uint16
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for uint16
if not 0 <= $value < 2**16:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_uint16($value)
""", value=name)

        return block, var["value"]

    def pack_int8(self, name):
        block, var = self.parse("""
# pack int8
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for int8
if not -2**7 <= $value < 2**7:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int8($value)
""", value=name)

        return block, var["value"]

    def pack_int16(self, name):
        block, var = self.parse("""
# pack int16
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for int16
if not -2**15 <= $value < 2**15:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int16($value)
""", value=name)

        return block, var["value"]

    def pack_int32(self, name):
        block, var = self.parse("""
# pack int32
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for int32
if not -2**31 <= $value < 2**31:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int32($value)
""", value=name)

        return block, var["value"]

    def pack_int64(self, name):
        block, var = self.parse("""
# pack int64
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for int64
if not -2**63 <= $value < 2**63:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_int64($value)
""", value=name)

        return block, var["value"]

    def pack_uint32(self, name):
        block, var = self.parse("""
# pack uint32
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for uint32
if not 0 <= $value < 2**32:
    raise ValueError("Value '$value' not in range")
$value = ctypes.c_uint32($value)
""", value=name)

        return block, var["value"]

    def pack_uint64(self, name):
        block, var = self.parse("""
# pack uint64
if not isinstance($value, basestring):
    $value = int($value)
else:
    raise TypeError

# overflow check for uint64
if not 0 <= $value < 2**64:
    raise ValueError("Value %r not in range" % $value)
$value = ctypes.c_uint64($value)
""", value=name)

        return block, var["value"]

    def setup_int64(self):
        block, var = self.parse("""
# new int64
$value = ctypes.c_int64()
""")
        return block, var["value"]

    def setup_uint64(self):
        block, var = self.parse("""
# new uint64
$value = ctypes.c_uint64()
""")
        return block, var["value"]

    def setup_uint32(self):
        block, var = self.parse("""
# new uint32
$value = ctypes.c_uint32()
""")
        return block, var["value"]

    def setup_int32(self):
        block, var = self.parse("""
# new int32
$value = ctypes.c_int32()
""")
        return block, var["value"]

    def setup_float(self):
        block, var = self.parse("""
# new float
$value = ctypes.c_float()
""")
        return block, var["value"]

    def setup_pointer(self):
        block, var = self.parse("""
# new pointer
$value = ctypes.c_void_p()
""")
        return block, var["value"]

    def setup_bool(self):
        block, var = self.parse("""
# new bool
$value = ctypes.c_bool()
""")
        return block, var["value"]

    def setup_uint8(self):
        block, var = self.parse("""
# new uint8
$value = ctypes.c_uint8()
""")
        return block, var["value"]

    def setup_int8(self):
        block, var = self.parse("""
# new int8
$value = ctypes.c_int8()
""")
        return block, var["value"]

    def setup_int16(self):
        block, var = self.parse("""
# new int16
$value = ctypes.c_int16()
""")
        return block, var["value"]

    def setup_uint16(self):
        block, var = self.parse("""
# new uint16
$value = ctypes.c_uint16()
""")
        return block, var["value"]

    def setup_string(self):
        block, var = self.parse("""
# new string
$value = ctypes.c_char_p()
""")

        return block, var["value"]

    def setup_double(self):
        block, var = self.parse("""
# new double
$value = ctypes.c_double()
""")

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
        gtype_map = {
            str: "gchararray",
            int: "gint",
            float: "gdouble",
            bool: "gboolean",
        }

        items = gtype_map.items()
        gtype_map = dict((k, PGType.from_name(v)) for (k, v) in items)

        block, var = self.parse("""
if not isinstance($obj, PGType):
    if hasattr($obj, "__gtype__"):
        $obj = $obj.__gtype__
    elif $obj in $gtype_map:
        $obj = $gtype_map[$obj]

if not isinstance($obj, PGType):
    raise TypeError("%r not a GType" % $obj)

$gtype = GType($obj._type.value)
""", gtype_map=gtype_map, obj=name)

        block.add_dependency("PGType", PGType)
        block.add_dependency("GType", GType)

        return block, var["gtype"]


class InterfaceTypes(object):

    def pack_enum(self, name, base_type):
        block, var = self.parse("""
if $val not in $base_type._allowed:
    raise TypeError("Invalid enum value %r" % $val)

$val = ctypes.c_uint($val)
""", base_type=base_type, val=name)

        return block, var["val"]

    def setup_enum(self):
        block, var = self.parse("""
$val = ctypes.c_uint()
""")
        return block, var["val"]

    def setup_flags(self):
        block, var = self.parse("""
$val = ctypes.c_uint()
""")
        return block, var["val"]

    def pack_flags(self, name, base_type):
        block, var = self.parse("""
# https://bugzilla.gnome.org/show_bug.cgi?id=693053
if not isinstance($var, basestring) and not int($var):
    $var = ctypes.c_uint()
elif not isinstance($var, $base_type):
    raise TypeError("Expected %r but got %r" % ($base_type.__name__, type($var).__name__))
else:
    $var = ctypes.c_uint(int($var))
""", var=name, base_type=base_type)

        return block, var["var"]

    def pack_callback(self, name, pack_func):
        block, var = self.parse("""
if not callable($py_cb):
    raise TypeError("%r must be callable" % $py_cb)
$ctypes_cb = $pack_func($py_cb)
""", pack_func=pack_func, py_cb=name)

        return block, var["ctypes_cb"]

    def ref_object_null(self, name):
        block, var = self.parse("""
# take ownership
if $obj:
    $obj._ref()
""", obj=name)
        return block

    def pack_object(self, obj_name, type_):
        block, var = self.parse("""
if not isinstance($obj, $type_class):
    raise TypeError("argument $obj: Expected %s, got %s" % ($type_class.__name__, $obj.__class__.__name__))
$ptr = ctypes.c_void_p($obj._obj)
""", obj=obj_name, type_class=type_)

        return block, var["ptr"]

    def pack_object_null(self, obj_name, type_):
        block, var = self.parse("""
if $obj is not None:
    if not isinstance($obj, $type_class):
        raise TypeError("argument $obj: Expected %s, got %s" % ($type_class.__name__, $obj.__class__.__name__))
    $ptr = ctypes.c_void_p($obj._obj)
else:
    $ptr = None
""", obj=obj_name, type_class=type_)

        return block, var["ptr"]

    def unpack_object(self, name):
        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = PGType(G_TYPE_FROM_INSTANCE(instance.contents))
            pytype = gtype.pytype
            if not pytype:
                raise RuntimeError("Couldn't find python type for %r" % gtype)
            return pytype

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
$obj = ctypes.c_void_p($obj._obj)
""", obj=name, base_struct_class=BaseStructure, base_obj_class=base_obj)

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


class CArrayTypes(object):

    def pack_carray_basic_fixed_zero(self, name, item_in, item_out, type_pack, type_, length):
        block, var = self.parse("""
if len($name) != $length:
    raise ValueError("Wrong list length")

$array = ($ctypes_type * ($length + 1))()
for $i, $item_in in enumerate($name):
    $type_pack
    $array[$i] = $item_out
$array[-1] = $ctypes_type()
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, type_pack=type_pack,
     ctypes_type=typeinfo_to_ctypes(type_), length=length)

        return block, var["array_ptr"]

    def pack_carray_basic_zero(self, name, item_in, item_out, type_pack, type_):
        block, var = self.parse("""
$length = len($name)
$array = ($ctypes_type * ($length + 1))()
for $i, $item_in in enumerate($name):
    $type_pack
    $array[$i] = $item_out
$array[-1] = $ctypes_type()
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, type_pack=type_pack,
     ctypes_type=typeinfo_to_ctypes(type_))

        return block, var["array_ptr"]

    def pack_carray_basic_length_zero(self, name, item_in, item_out, type_pack, type_, length_type_):
        block, var = self.parse("""
$length = len($name)
$c_length = $length_type($length)
$array = ($ctypes_type * ($length + 1))()
for $i, $item_in in enumerate($name):
    $type_pack
    $array[$i] = $item_out
$array[-1] = $ctypes_type()
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, type_pack=type_pack,
     ctypes_type=typeinfo_to_ctypes(type_),
     length_type=typeinfo_to_ctypes(length_type_))

        return block, var["array_ptr"], var["c_length"]

    def pack_carray_basic_length(self, name, item_in, item_out, type_pack, type_, length_type_):
        block, var = self.parse("""
$length = len($name)
$c_length = $length_type($length)
$array = ($ctypes_type * $length)()
for $i, $item_in in enumerate($name):
    $type_pack
    $array[$i] = $item_out
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, type_pack=type_pack,
     ctypes_type=typeinfo_to_ctypes(type_),
     length_type=typeinfo_to_ctypes(length_type_))

        return block, var["array_ptr"], var["c_length"]

    def pack_carray_basic_fixed(self, name, item_in, item_out, type_pack, type_, length):
        block, var = self.parse("""
if len($name) != $length:
    raise ValueError("Wrong list length")

$array = ($ctypes_type * $length)()
for $i, $item_in in enumerate($name):
    $type_pack
    $array[$i] = $item_out
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, type_pack=type_pack,
     ctypes_type=typeinfo_to_ctypes(type_), length=length)

        return block, var["array_ptr"]

    def setup_carray_basic_fixed(self, length, type_):
        block, var = self.parse("""
$array = ($ctypes_type * $length)()
$array_ptr = ctypes.pointer($array)
""", ctypes_type=typeinfo_to_ctypes(type_), length=length)

        return block, var["array"], var["array_ptr"]

    def unpack_carray_basic_fixed(self, array, length):
        block, var = self.parse("""
$out = [$array[$i] for $i in xrange($length)]
""", array=array, length=length)

        return block, var["out"]

    def unpack_carray_basic_length(self, array, length):
        block, var = self.parse("""
$out = [$array[$i] for $i in xrange($length.value)]
""", array=array, length=length)

        return block, var["out"]

    def unpack_carray_zeroterm(self, in_name):
        block, var = self.parse("""
$list = []
$i = 0
$current = $array and $array[$i]
while $current:
    $list.append($current)
    $i += 1
    $current = $array[$i]
""", array=in_name)

        return block, var["list"]


class ErrorTypes(object):

    def setup_gerror(self):
        block, var = self.parse("""
$ptr = $gerror_ptr()
""", gerror_ptr=GErrorPtr)

        return block, var["ptr"]

    def unpack_gerror(self, name):
        block, var = self.parse("""
if $gerror_ptr:
    $out = PGError($gerror_ptr.contents)
else:
    $out = None
""", gerror_ptr=name)

        block.add_dependency("PGError", PGError)
        return block, var["out"]

    def raise_gerror(self, name):
        block, var = self.parse("""
if $var:
    raise $var
""", var=name)

        return block

    def free_gerror(self, name):
        block, var = self.parse("""
if $ptr:
    $ptr.free()
""", ptr=name)
        return block


class CTypesBackend(CodeGenBackend, BasicTypes, InterfaceTypes, CArrayTypes,
                    ErrorTypes):

    NAME = "ctypes"

    def __init__(self, *args, **kwargs):
        CodeGenBackend.__init__(self, *args, **kwargs)
        self._libs = {}

    def parse(self, *args, **kwargs):
        block, var = CodeGenBackend.parse(self, *args, **kwargs)
        block.add_dependency("ctypes", ctypes)
        return block, var

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
        try:
            h = getattr(lib, symbol)
        except AttributeError:
            raise NotImplementedError(
                "Library doesn't provide symbol: %s" % symbol)

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

    def call(self, func, args):
        block, var = self.parse("""
try:
    $ret = $name($args)
except ctypes.ArgumentError, $e:
    raise TypeError($e.message)
""", name=func, args=args)

        return block, var["ret"]

    def cast_pointer(self, name, type_):
        block, var = self.parse("""
$value = ctypes.cast($value, ctypes.POINTER($type))
""", value=name, type=typeinfo_to_ctypes(type_))

        return block, name

    def free_pointer(self, name):
        block, var = self.parse("""
glib.free($ptr)
""", ptr=name)

        block.add_dependency("glib", glib)
        return block

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

        return block, var["ptr"]

    def get_callback_object(self, func, args, ret=None):
        arg_types = [typeinfo_to_ctypes(a.type) for a in args]
        # FIXME.. don't ignore missing ret
        ret_type = ret and typeinfo_to_ctypes(ret.type)
        cb_object_type = ctypes.CFUNCTYPE(ret_type, *arg_types)
        return ctypes.cast(cb_object_type(func), GCallback)
