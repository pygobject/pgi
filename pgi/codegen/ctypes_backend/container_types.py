# Copyright 2012-2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib.gir import GITypeTag
from pgi.clib import glib

from .utils import BaseType, register_type, typeinfo_to_ctypes


@register_type(GITypeTag.GLIST)
class GList(BaseType):

    def check(self, name):
        pass

    def pack(self, name):
        param_type_info = self.type.get_param_type(0)
        param_type = self.get_type(param_type_info)

        param_in = self.var()
        param_out = param_type.pack_pointer(param_type.check(param_in))

        return self.parse("""
$new = $GListPtr()
for $item in $seq:
    $param_check_pack
    $new = $new.prepend($item_out)
$new = $new.reverse()
""", seq=name, GListPtr=glib.GListPtr, item=param_in,
param_check_pack=param_type.block, item_out=param_out)["new"]

    def unpack(self, name):
        param_type = self.type.get_param_type(0)
        ctypes_type = typeinfo_to_ctypes(param_type)

        p = self.get_type(param_type)
        item_in = self.var()
        item_out = p.unpack(item_in)

        return self.parse("""
$out = []
$elm = $in_
while $elm:
    $entry = $elm.contents
    $item_in = $ctypes_type($entry.data or 0).value
    $item_unpack
    $out.append($item_out)
    $elm = $entry.next
""", in_=name, ctypes_type=ctypes_type, item_in=item_in,
item_out=item_out, item_unpack=p.block)["out"]

    def free(self, name):
        return self.parse("""
$list_.free()
""", list_=name)


@register_type(GITypeTag.GSLIST)
class GSList(BaseType):
    pass
