# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.fields import get_field_class
from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock


def _generate_field_setter(info, info_type, backend):
    cls = get_field_class(info_type)
    f = cls(info, info_type, backend)
    main = CodeBlock()
    main.write_line("def setter(instance, value):")

    if info.offset:
        main.write_line("pointer = instance._obj + %d" % info.offset, 1)
    else:
        main.write_line("pointer = instance._obj", 1)

    block, ptr = backend.cast_pointer("pointer", info_type)
    block.write_into(main, 1)

    block, var = f.set(ptr, "value")
    if block:
        block.write_into(main, 1)

    block = backend.assign_pointer(ptr, var)
    block.write_into(main, 1)

    func = main.compile()["setter"]
    func._code = main

    return func


def _generate_field_getter(info, info_type, backend):
    cls = get_field_class(info_type)
    f = cls(info, info_type, backend)

    main = CodeBlock()
    main.write_line("def getter(instance):")

    if info.offset:
        # gi docs are lying, offset in bytes
        main.write_line("pointer = instance._obj + %d" % info.offset, 1)
    else:
        main.write_line("pointer = instance._obj", 1)

    # uh.. too much logic here..
    block, var = backend.cast_pointer("pointer", info_type)
    block.write_into(main, 1)
    block, var = backend.deref_pointer(var)
    block.write_into(main, 1)
    block, var = backend.unpack_basic(var)
    block.write_into(main, 1)

    block, var = f.get(var)
    if block:
        block.write_into(main, 1)
    main.write_line("return %s" % var, 1)
    func = main.compile()["getter"]
    func._code = main

    return func


def _generate_field_access(info, setter=True):
    info_type = info.get_type()

    func = None
    messages = []
    for backend in ACTIVE_BACKENDS:
        try:
            if setter:
                func = _generate_field_setter(info, info_type, backend)
            else:
                func = _generate_field_getter(info, info_type, backend)
        except NotImplementedError, e:
            messages.append("%s: %s" % (backend.NAME, e.message))
        else:
            break

    if func:
        return func

    raise NotImplementedError("\n".join(messages))


def generate_field_getter(info):
    return _generate_field_access(info, setter=False)


def generate_field_setter(info):
    return _generate_field_access(info, setter=True)
