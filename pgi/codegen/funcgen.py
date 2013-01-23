# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock
from pgi.util import escape_name, escape_builtin
from pgi.codegen.arguments import get_argument_class, ErrorArgument
from pgi.codegen.returnvalues import get_return_class


def _generate_function(backend, info, arg_infos, arg_types,
                       return_type, method, throws):
    main = CodeBlock()

    main.write_line("# backend: %s" % backend.NAME)

    cls = get_return_class(return_type)
    return_value = cls(info, return_type, backend)

    args = []
    for arg_info, arg_type in zip(arg_infos, arg_types):
        cls = get_argument_class(arg_type)
        name = escape_name(escape_builtin(arg_info.name))
        args.append(cls(name, args, backend, arg_info, arg_type))

    if throws:
        args.append(ErrorArgument(args, backend))

    # setup
    for arg in args:
        arg.setup()

    # generate header
    names = [a.in_var for a in args if not a.is_aux and a.in_var]
    if method:
        names.insert(0, "self")
    f = "def %s(%s):" % (info.name, ", ".join(names))
    main.write_line(f)

    docstring = "%s(%s)" % (info.name, ", ".join(names))

    for arg in args:
        if arg.is_aux:
            continue
        block = arg.pre_call()
        if block:
            block.write_into(main, 1)

    # generate call
    lib = backend.get_library_object(info.namespace)
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
    block, return_var = return_value.process(ret)
    if block:
        block.write_into(main, 1)
    if return_var:
        out.append(return_var)

    # process out args
    for arg in args:
        if arg.is_aux:
            continue
        block = arg.post_call()
        if block:
            block.write_into(main, 1)
        if arg.out_var:
            out.append(arg.out_var)

    if len(out) == 1:
        main.write_line("return %s" % out[0], 1)
    elif len(out) > 1:
        main.write_line("return (%s)" % ", ".join(out), 1)

    func = main.compile()[info.name]
    func._code = main
    func.__doc__ = docstring

    return func


def generate_function(info, method=False, throws=False):
    arg_infos = info.get_args()
    arg_types = [a.get_type() for a in arg_infos]
    return_type = info.get_return_type()

    func = None
    messages = []
    for backend in ACTIVE_BACKENDS:
        try:
            func = _generate_function(backend, info, arg_infos, arg_types,
                                      return_type, method, throws)
        except NotImplementedError, e:
            messages.append("%s: %s" % (backend.NAME, e.message))
        else:
            break

    return_type.unref()
    for info in arg_infos:
        info.unref()
    for info in arg_types:
        info.unref()

    if func:
        return func

    raise NotImplementedError("\n".join(messages))
