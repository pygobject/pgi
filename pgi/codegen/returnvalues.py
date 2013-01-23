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
        return None, None

    def is_zero_terminated(self):
        return self.type.is_zero_terminated

    def is_pointer(self):
        return self.type.is_pointer


class BooleanReturnValue(ReturnValue):
    TAG = GITypeTag.BOOLEAN

    def process(self, name):
        return self.backend.unpack_bool(name)


class VoidReturnValue(ReturnValue):
    TAG = GITypeTag.VOID

    def process(self, name):
        if self.is_pointer():
            return None, name
        else:
            return None, None


class ArrayReturnValue(ReturnValue):
    TAG = GITypeTag.ARRAY

    def process(self, name):
        backend = self.backend
        if self.is_zero_terminated():
            block, var = backend.unpack_array_zeroterm_c(name)
            return block, var

        raise NotImplementedError


class UInt8ReturnValue(ReturnValue):
    TAG = GITypeTag.INT8

    def process(self, name):
        return None, name


class Int32ReturnValue(ReturnValue):
    TAG = GITypeTag.INT32

    def process(self, name):
        return None, name


class Int64ReturnValue(ReturnValue):
    TAG = GITypeTag.INT64

    def process(self, name):
        return None, name


class UInt64ReturnValue(ReturnValue):
    TAG = GITypeTag.UINT64

    def process(self, name):
        return None, name


class UInt32ReturnValue(ReturnValue):
    TAG = GITypeTag.UINT32

    def process(self, name):
        return None, name


class UInt8ReturnValue(ReturnValue):
    TAG = GITypeTag.UINT8

    def process(self, name):
        return None, name


class DoubleReturnValue(ReturnValue):
    TAG = GITypeTag.DOUBLE

    def process(self, name):
        return None, name


class FloatReturnValue(ReturnValue):
    TAG = GITypeTag.FLOAT

    def process(self, name):
        return None, name


class Utf8ReturnValue(ReturnValue):
    TAG = GITypeTag.UTF8

    def process(self, name):
        return self.backend.unpack_string(name)


class FilenameReturnValue(Utf8ReturnValue):
    TAG = GITypeTag.FILENAME

    def process(self, name):
        return self.backend.unpack_string(name)


class InterfaceReturnValue(ReturnValue):
    TAG = GITypeTag.INTERFACE

    def process(self, name):
        backend = self.backend
        iface = self.type.get_interface()
        iface_type = iface.type.value
        iface_namespace = iface.namespace
        iface_name = iface.name
        iface.unref()

        if iface_type == GIInfoType.ENUM:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_enum(name, attr)
        elif iface_type == GIInfoType.OBJECT:
            return backend.unpack_object(name)
        elif iface_type == GIInfoType.STRUCT:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_struct(name, attr)
        elif iface_type == GIInfoType.UNION:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_union(name, attr)
        elif iface_type == GIInfoType.FLAGS:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_flags(name, attr)

        raise NotImplementedError(
            "Unsuported interface return type %r" % iface.type)


class GTypeReturnValue(ReturnValue):
    TAG = GITypeTag.GTYPE

    def process(self, name):
        return self.backend.unpack_gtype(name)


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
    tag_value = type_.tag.value
    try:
        return _classes[tag_value]
    except KeyError:
        raise NotImplementedError("%r return not implemented" % type_.tag)
