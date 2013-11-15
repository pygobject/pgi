# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""
A no op backend that can be used to introspect parts of the bindings
that aren't supported by other backends.

Example usage: pgi.set_backend("ctypes,cffi,null")
A working backend is still needed to init some modules (Gtk/Gst.init..)
"""

from .backend import VariableFactory
from pgi.clib.gir import GITypeTag
from .utils import CodeBlock, parse_with_objects


class BaseType(object):
    block = CodeBlock()

    def __init__(self, type_):
        self.type = type_

    def pack(self, name, *args):
        if args:
            return (name, None)
        return name

    def free(self, *args):
        pass

    def check_raise(self, *args):
        pass

    def check(self, name):
        return name

    def new(self, *args):
        if self.type.tag.value == GITypeTag.ARRAY:
            return ("new", "new2")
        return "new"

    def get_reference(self, name):
        return name

    def unpack(self, name, *args):
        return name

    def pre_unpack(self, name):
        return name

    def pack_in(self, name):
        return name

    def unpack_return(self, name):
        return name

    def unpack_gvalue(self, name):
        return name

    def ref(self, *args):
        pass

    def alloc(self):
        return "new"


class NullBackend(object):
    NAME = "null"

    def get_library(self, namespace):
        return namespace

    def get_function(self, *args, **kwargs):
        return CodeBlock(), "foo", lambda *x: None

    def get_type(self, type_, *args, **kwargs):
        return BaseType(type_)

    def parse(self, code, **kwargs):
        return parse_with_objects(code, VariableFactory(), **kwargs)

    def cast_pointer(self, name, *args):
        return CodeBlock(), name

    def assign_pointer(self, ptr, *args):
        return CodeBlock(), ptr

    def deref_pointer(self, name):
        return CodeBlock(), name
