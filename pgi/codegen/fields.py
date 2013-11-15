# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib.gir import GIInfoType, GITypeTag


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
        var = self.backend.get_type(self.type)
        iface = self.type.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.ENUM:
            out = var.unpack(var.pre_unpack(name))
            return var.block, out
        elif iface_type == GIInfoType.STRUCT:
            out = var.unpack(var.pre_unpack(name))
            return var.block, out
        elif iface_type == GIInfoType.OBJECT:
            out = var.unpack(name)
            return var.block, out
        elif iface_type == GIInfoType.FLAGS:
            out = var.unpack(var.pre_unpack(name))
            return var.block, out

        raise NotImplementedError(
            "interface type not supported: %r" % iface.type)


class TypeField(Field):
    TAG = GITypeTag.GTYPE

    def get(self, name):
        var = self.backend.get_type(self.type)
        out = var.unpack(var.pre_unpack(name))
        return var.block, out


class BasicField(Field):

    def get(self, name):
        var = self.backend.get_type(self.type)
        out = var.unpack(var.pre_unpack(name))
        return var.block, out

    def set(self, name, value_name):
        var = self.backend.get_type(self.type)
        out = var.pack(value_name)
        return var.block, out


class DoubleField(BasicField):
    TAG = GITypeTag.DOUBLE


class UInt32Field(BasicField):
    TAG = GITypeTag.UINT32


class UInt8Field(BasicField):
    TAG = GITypeTag.UINT8


class Int32Field(BasicField):
    TAG = GITypeTag.INT32


class Int64Field(BasicField):
    TAG = GITypeTag.INT64


class UInt16Field(BasicField):
    TAG = GITypeTag.UINT16


class Int16Field(BasicField):
    TAG = GITypeTag.INT16


class FloatField(BasicField):
    TAG = GITypeTag.FLOAT


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
