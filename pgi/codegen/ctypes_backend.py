# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.codegen.backend import CodeGenBackend
from pgi.codegen.utils import CodeBlock
from pgi.gir import GIRepositoryPtr
from pgi.glib import GErrorPtr
from pgi.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr
from pgi.util import typeinfo_to_ctypes, import_attribute
from pgi.gtype import PGType


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

    def unpack_string(self, name):
        return CodeBlock(), name

    def pack_bool(self, name):
        block, var = self.parse("""
$boolean = bool($var) # https://bugs.pypy.org/issue1367
""", var=name)

        return block, var["boolean"]

    def unpack_bool(self, name):
        return None, name

    def unpack_basic_ptr(self, name):
        block, var = self.parse("""
# unpack basic pointer
$value = $ctypes_value.value
""", ctypes_value=name)

        block.add_dependency("ctypes", ctypes)
        return block, var["value"]

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

    def pack_uint32_ptr(self):
        block, var = self.parse("""
# pack uint32
$uint = ctypes.c_uint32()
$uint_ref = ctypes.byref($uint)
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["uint"], var["uint_ref"]

    def pack_float_ptr(self):
        block, var = self.parse("""
# pack float
$float = ctypes.c_float()
$float_ref = ctypes.byref($float)
""")

        block.add_dependency("ctypes", ctypes)
        return block, var["float"], var["float_ref"]

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

    def unpack_enum(self, name, type_):
        type_var = self.var()

        block, var = self.parse("""
# unpack enum
$enum = $enum_class($value)
""", enum_class=type_var, value=name)

        block.add_dependency(type_var, type_)
        return block, var["enum"]


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
            h.restype = typeinfo_to_ctypes(ret.type)
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
