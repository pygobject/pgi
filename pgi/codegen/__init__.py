# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.arguments import get_argument_class
from pgi.codegen.returnvalues import get_return_class
from pgi.codegen.utils import CodeBlock, CodeGenerator
from pgi.codegen.ctypes_backend import CTypesBackend


def generate_function(info, namespace, name, method=False):
    main = CodeBlock()

    def var_factory():
        var_factory.c += 1
        return "t%d" % var_factory.c
    var_factory.c = 0

    parser = CodeGenerator(var_factory)
    backend = CTypesBackend(parser)

    return_type = info.get_return_type()
    cls = get_return_class(return_type)
    return_value = cls(info, return_type, backend)

    args = []
    arg_infos = info.get_args()
    arg_types = []
    for arg_info in arg_infos:
        arg_type = arg_info.get_type()
        arg_types.append(arg_type)
        cls = get_argument_class(arg_type)
        args.append(cls(arg_info, arg_type, args, backend))

    # setup
    for arg in args:
        arg.setup()

    # generate header
    names = [a.name for a in args if not a.is_aux]
    if method:
        names.insert(0, "self")
    f = "def %s(%s):" % (name, ", ".join(names))
    main.write_line(f)

    for arg in args:
        if arg.is_aux:
            continue
        block = arg.pre_call()
        if block:
            block.write_into(main, 1)

    # generate call
    lib = backend.get_library_object(namespace)
    symbol = info.get_symbol()
    func = backend.get_function_object(lib, symbol, args, return_value)

    call_vars = [a.call_var for a in args if a.call_var]
    if method:
        call_vars.insert(0, "self._obj")
    block, ret = backend.call("func", ", ".join(call_vars))
    block.add_dependency("func", func)
    block.write_into(main, 1)

    out = []

    # process return value
    block, return_var = return_value.process(ret)
    if return_var:
        out.append(return_var)
    if block:
        block.write_into(main, 1)

    # process out args
    for arg in args:
        if arg.is_aux:
            continue
        arg.post_call()
        out += arg.out_vars

    if len(out) == 1:
        main.write_line("return %s" % out[0], 1)
    elif len(out) > 1:
        main.write_line("return (%s, %s)" % (ret, ", ".join(out)), 1)

    return_type.unref()
    for info in arg_infos:
        info.unref()
    for info in arg_types:
        info.unref()

    return main.compile()[name]
