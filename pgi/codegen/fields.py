# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GIInfoType, GITypeTag
from pgi.util import import_attribute


class Field(object):
    TAG = None

    def __init__(self, info, type, backend):
        self.backend = backend
        self.info = info
        self.type = type

    def get(self, name):
        raise NotImplementedError("no getter implemented")

    def set(self, name, value_name):
        raise NotImplementedError("no setter implemented")


class InterfaceField(Field):
    TAG = GITypeTag.INTERFACE

    def get(self, name):
        backend = self.backend
        iface = self.type.get_interface()
        iface_type = iface.type.value
        iface_namespace = iface.namespace
        iface_name = iface.name
        iface.unref()

        if iface_type == GIInfoType.ENUM:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_enum(name, attr)
        elif iface_type == GIInfoType.STRUCT:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_struct(name, attr)

        raise NotImplementedError("interface type not supported")


class TypeField(Field):
    TAG = GITypeTag.GTYPE

    def get(self, name):
        return self.backend.unpack_gtype(name)


class DoubleField(Field):
    TAG = GITypeTag.DOUBLE

    def get(self, name):
        return None, name


class UInt16Field(Field):
    TAG = GITypeTag.UINT16

    def set(self, name, value_name):
        return self.backend.pack_uint16(value_name)

    def get(self, name):
        return None, name

_classes = {}


def _find_fields():
    global _classes
    cls = [a for a in globals().values() if isinstance(a, type)]
    args = [a for a in cls if issubclass(a, Field) and a is not Field]
    _classes = dict(((a.TAG, a) for a in args))
_find_fields()


def get_field_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    try:
        return _classes[tag_value]
    except KeyError:
        raise NotImplementedError("%r not supported" % arg_type.tag)
