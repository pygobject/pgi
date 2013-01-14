# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GITypeTag, GIInfoType
from pgi.util import import_attribute


class ReturnValue(object):
    TAG = None

    def __init__(self, info, type_, backend):
        super(ReturnValue, self).__init__()
        self.info = info
        self.type = type_
        self.backend = backend

    def process(self, name):
        return None, name

    def is_zero_terminated(self):
        return self.type.is_zero_terminated()


class VoidReturnValue(ReturnValue):
    TAG = GITypeTag.VOID

    def process(self, name):
        return None, None


class ArrayReturnValue(ReturnValue):
    TAG = GITypeTag.ARRAY

    def process(self, name):
        backend = self.backend
        if self.is_zero_terminated():
            block, var = backend.unpack_array_zeroterm_c(name)
            return block, var


class InterfaceReturnValue(ReturnValue):
    TAG = GITypeTag.INTERFACE

    def process(self, name):
        backend = self.backend
        iface = self.type.get_interface()
        iface_type = iface.get_type().value
        iface_namespace = iface.get_namespace()
        iface_name = iface.get_name()
        iface.unref()
        if iface_type == GIInfoType.ENUM:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_enum(name, attr)
        return None, name


_classes = {}


def _find_return_values():
    global _classes
    cls = [a for a in globals().values() if isinstance(a, type)]
    rv = ReturnValue
    retv = [a for a in cls if issubclass(a, rv) and a is not rv]
    _classes = dict(((a.TAG, a) for a in retv))
_find_return_values()


def get_return_class(type_):
    global _classes
    tag_value = type_.get_tag().value
    return _classes.get(tag_value, ReturnValue)
