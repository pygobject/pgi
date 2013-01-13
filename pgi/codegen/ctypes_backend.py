# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.codegen.backend import CodeGenBackend
from pgi.gir import GIRepositoryPtr
from pgi.util import typeinfo_to_ctypes


class CTypesBackend(CodeGenBackend):

    def get_library_object(self, namespace):
        paths = GIRepositoryPtr().get_shared_library(namespace)
        if not paths:
            return
        path = paths.split(",")[0]
        return getattr(ctypes.cdll, path)

    def get_function_object(self, lib, symbol, args, ret):
        h = getattr(lib, symbol)
        h.restype = typeinfo_to_ctypes(ret.type)

        arg_types = []
        for arg in args:
            type_ = typeinfo_to_ctypes(arg.type)
            # FIXME: cover all types..
            if not type_:
                continue
            if arg.is_direction_out() and type_ != ctypes.c_void_p:
                type_ = ctypes.POINTER(type_)
            arg_types.append(type_)

        h.argtypes = arg_types
        return h

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

    def pack_interface(self, name):
        block, var = self.parse("""
$obj = ctypes.cast($iface._obj, ctypes.c_void_p)
""")
        block.add_dependency("ctypes", ctypes)

        return block, var["obj"]

    def pack_array_ptr_fixed_c(self, name):
        block, var = self.parse("""
# pack char array
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
