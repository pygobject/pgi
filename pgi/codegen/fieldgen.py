# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GIInfoType, GITypeTag
from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock, parse_code
from pgi.util import import_attribute


class FieldAccess(object):
    TAG = GITypeTag.INTERFACE

    def __init__(self, info, type, backend):
        self.backend = backend
        self.info = info
        self.type = type

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

    def set(self):
        raise NotImplementedError("no setter implemted")


def generate_field_getter(info):
    # only ctypes for now
    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break

    type_ = info.get_type()

    if type_.tag.value != FieldAccess.TAG:
        type_.unref()
        raise NotImplementedError("Only interface getters supported")

    f = FieldAccess(info, type_, backend)

    main = CodeBlock()
    main.write_line("def getter(argument):")
    main.write_line("argument = argument._obj", 1)

    # no idea if that works
    if info.offset:
        main.write_line("argument = argument + %d", info.offset / 8, 1)

    # uh.. too much logic here..
    block, var = backend.cast_pointer("argument", type_)
    block.write_into(main, 1)
    block, var = backend.deref_pointer(var)
    block.write_into(main, 1)
    block, var = backend.unpack_basic_ptr(var)
    block.write_into(main, 1)

    block, var = f.get(var)
    block.write_into(main, 1)
    main.write_line("return %s" % var, 1)

    func = main.compile()["getter"]

    type_.unref()

    return func
