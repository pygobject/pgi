# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GITypeTag, GIInfoType, GIDirection, GITransfer
from pgi.util import import_attribute


class CallbackArgument(object):
    TAG = None

    is_aux = False

    def __init__(self, backend, info, type_, name):
        self.info = info
        self.name = name
        self.backend = backend
        self.type = type_

    @classmethod
    def get_class(cls):
        return cls

    def setup(self):
        pass

    def process(self):
        return None, self.name

    def may_be_null(self):
        return self.info.may_be_null

    def is_pointer(self):
        return self.type.is_pointer

    def is_direction_in(self):
        return self.direction in (GIDirection.INOUT, GIDirection.IN)

    def is_direction_out(self):
        return self.direction in (GIDirection.INOUT, GIDirection.OUT)

    def is_direction_inout(self):
        return self.direction == GIDirection.INOUT

    def transfer_nothing(self):
        return self.info.ownership_transfer.value == GITransfer.NOTHING

    def transfer_container(self):
        return self.info.ownership_transfer.value == GITransfer.CONTAINER

    def transfer_everything(self):
        return self.info.ownership_transfer.value == GITransfer.EVERYTHING


class InterfaceArgument(CallbackArgument):
    TAG = GITypeTag.INTERFACE

    def process(self):
        backend = self.backend
        iface = self.type.get_interface()
        iface_type = iface.type.value
        iface_namespace = iface.namespace
        iface_name = iface.name

        if iface_type == GIInfoType.OBJECT:
            return backend.unpack_object(self.name)
        elif iface_type == GIInfoType.UNION:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_union(self.name, attr)
        elif iface_type == GIInfoType.STRUCT:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_struct(self.name, attr)
        elif iface_type == GIInfoType.FLAGS:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_flags(self.name, attr)

        raise NotImplementedError("interface %r not supported" % iface.type)


class Utf8Argument(CallbackArgument):
    TAG = GITypeTag.UTF8


class VoidArgument(CallbackArgument):
    TAG = GITypeTag.VOID


_classes = {}
def _find_cbargs():
    global _classes
    for var in globals().values():
        if not isinstance(var, type):
            continue
        if issubclass(var, CallbackArgument) and var is not CallbackArgument:
            _classes[var.TAG] = var
_find_cbargs()


def get_cbarg_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    try:
        cls = _classes[tag_value]
    except KeyError:
        raise NotImplementedError(
            "%r signal argument not implemented" % arg_type.tag)
    else:
        return cls.get_class()
