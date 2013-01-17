# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock
from pgi.codegen.arguments import get_argument_class, ErrorArgument
from pgi.codegen.returnvalues import get_return_class, VoidReturnValue


def _generate_function(backend, info, namespace, name, method, throws):
    main = CodeBlock()

    main.write_line("# backend: %s" % backend.NAME)

    return_type = info.get_return_type()
    cls = get_return_class(return_type)
    if cls is VoidReturnValue:
        return_value = None
    else:
        return_value = cls(info, return_type, backend)

    args = []
    arg_infos = info.get_args()

    arg_types = []
    for arg_info in arg_infos:
        arg_type = arg_info.get_type()
        arg_types.append(arg_type)
        cls = get_argument_class(arg_type)
        args.append(cls(arg_info, arg_type, args, backend))

    if throws:
        args.append(ErrorArgument(None, None, args, backend))

    # setup
    for arg in args:
        arg.setup()

    # generate header
    names = [a.name for a in args if not a.is_aux and a.is_direction_in()]
    if method:
        names.insert(0, "self")
    f = "def %s(%s):" % (name, ", ".join(names))
    main.write_line(f)

    docstring = "%s(%s)" % (name, ", ".join(names))

    for arg in args:
        if arg.is_aux:
            continue
        block = arg.pre_call()
        if block:
            block.write_into(main, 1)

    # generate call
    lib = backend.get_library_object(namespace)
    symbol = info.symbol
    block, svar, func = backend.get_function_object(lib, symbol, args,
                                                    return_value, method,
                                                    "self", throws)
    if block:
        block.write_into(main, 1)

    call_vars = [a.call_var for a in args if a.call_var]
    if method:
        call_vars.insert(0, svar)
    block, ret = backend.call("func", ", ".join(call_vars))
    block.add_dependency("func", func)
    block.write_into(main, 1)

    out = []

    # handle errors first
    if throws:
        error_arg = args.pop()
        block = error_arg.post_call()
        if block:
            block.write_into(main, 1)

    # process return value
    if return_value:
        block, return_var = return_value.process(ret)
        if block:
            block.write_into(main, 1)
        out.append(return_var)

    # process out args
    for arg in args:
        if arg.is_aux:
            continue
        block = arg.post_call()
        if block:
            block.write_into(main, 1)
        out += arg.out_vars

    if len(out) == 1:
        main.write_line("return %s" % out[0], 1)
    elif len(out) > 1:
        main.write_line("return (%s)" % ", ".join(out), 1)

    return_type.unref()
    for info in arg_infos:
        info.unref()
    for info in arg_types:
        info.unref()

    func = main.compile()[name]
    func._code = main
    func.__doc__ = docstring

    return func


def generate_function(info, namespace, name, method=False, throws=False):
    for backend in ACTIVE_BACKENDS:
        try:
            return _generate_function(backend, info, namespace,
                                      name, method, throws)
        except NotImplementedError:
            continue
    raise NotImplementedError
