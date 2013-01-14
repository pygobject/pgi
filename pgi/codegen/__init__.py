# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.arguments import get_argument_class
from pgi.codegen.returnvalues import get_return_class, VoidReturnValue
from pgi.codegen.utils import CodeBlock

from pgi.codegen.ctypes_backend import CTypesBackend
try:
    from pgi.codegen.cffi_backend import CFFIBackend
except ImportError:
    CFFIBackend = None


BACKENDS = [CFFIBackend, CTypesBackend]
BACKENDS = filter(None, BACKENDS)
ACTIVE_BACKENS = BACKENDS


def set_backend(name=None):
    """Set a prefered ffi backend (cffi, ctypes).

    set_backend() -- default
    set_backend("cffi") -- cffi first, others as fallback
    set_backend("ctypes") -- ctypes first, others as fallback
    """

    possible = list(BACKENDS)
    if name is None:
        names = []
    else:
        names = name.split(",")
    for name in reversed(names):
        for backend in BACKENDS:
            if backend.NAME == name:
                possible.remove(backend)
                possible.insert(0, backend)
                break
        else:
            raise LookupError("Unkown backend: %r" % name)

    ACTIVE_BACKENS[:] = possible


def _generate_function(backend, info, namespace, name, method):
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

    # setup
    for arg in args:
        arg.setup()

    # generate header
    names = [a.name for a in args if not a.is_aux and a.is_in]
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
    symbol = info.get_symbol()
    block, func = backend.get_function_object(lib, symbol, args,
                                              return_value, method)
    if block:
        block.write_into(main, 1)

    call_vars = [a.call_var for a in args if a.call_var]
    if method:
        call_vars.insert(0, "self._obj")
    block, ret = backend.call("func", ", ".join(call_vars))
    block.add_dependency("func", func)
    block.write_into(main, 1)

    out = []

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


def generate_function(info, namespace, name, method=False):
    for backend_type in BACKENDS:
        try:
            backend = backend_type()
            return _generate_function(backend, info, namespace, name, method)
        except NotImplementedError:
            continue
    raise NotImplementedError
