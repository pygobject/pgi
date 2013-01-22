# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.fields import get_field_class
from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock, parse_code



def generate_field_getter(info):
    # only ctypes for now
    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break

    type_ = info.get_type()

    cls = get_field_class(type_)
    f = cls(info, type_, backend)

    main = CodeBlock()
    main.write_line("def getter(argument):")
    main.write_line("argument = argument._obj", 1)

    if info.offset:
        # gi docs are lying, offset in bytes
        main.write_line("argument = argument + %d" % info.offset, 1)

    # uh.. too much logic here..
    block, var = backend.cast_pointer("argument", type_)
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

    type_.unref()

    return func
