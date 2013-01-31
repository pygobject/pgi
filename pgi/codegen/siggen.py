# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock
from pgi.codegen.cbargs import get_cbarg_class
from pgi.util import escape_name, escape_builtin


def generate_callback(info):
    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break

    args = info.get_args()
    arg_types = [a.get_type() for a in args]

    cb_args = []
    for arg, type_ in zip(args, arg_types):
        cls = get_cbarg_class(type_)
        excaped_name = escape_builtin(escape_name(arg.name))
        cb_arg = cls(backend, arg, type_, excaped_name)
        cb_args.append(cb_arg)

    for arg in cb_args:
        arg.setup()

    body = CodeBlock()

    outs_vars = []
    for arg in cb_args:
        if arg.is_aux:
            continue
        block, out = arg.process()
        if block:
            block.write_into(body)
        outs_vars.append(out)

    argument_list = ", ".join([a.name for a in cb_args])
    forward_arguments = ", ".join(outs_vars)
    func_name = escape_name(info.name)
    cb_name = backend._var()

    block, var = backend.parse("""
def $cb_wrapper($args):
    $body
    $ret = $callback($out_args)
    # FIXME: convert return value
""", args=argument_list, out_args=forward_arguments, cb_wrapper=func_name,
     callback=cb_name, body=body)

    def create_cb_for_func(real_func):
        # binds the callback to the block and compiles it
        func = block.compile(**{cb_name: real_func})[func_name]
        return backend.get_callback_object(func, cb_args)

    return create_cb_for_func


def _generate_signal_callback(backend, info, args, arg_types):
    sig_args = []

    for arg, type_ in zip(args, arg_types):
        cls = get_cbarg_class(type_)
        excaped_name = escape_builtin(escape_name(arg.name))
        sig_arg = cls(backend, arg, type_, excaped_name)
        sig_args.append(sig_arg)

    for arg in sig_args:
        arg.setup()

    body = CodeBlock()

    outs_vars = []
    for arg in sig_args:
        if arg.is_aux:
            continue
        block, out = arg.process()
        if block:
            block.write_into(body)
        outs_vars.append(out)

    argument_list = ", ".join([a.name for a in sig_args])
    forward_arguments = ", ".join(outs_vars)
    func_name = escape_name(info.name)
    cb_name = backend._var()

    block, var = backend.parse("""
def $cb_wrapper($args):
    $body
    $ret = $callback($out_args)
    # FIXME: convert return value
""", args=argument_list, out_args=forward_arguments, cb_wrapper=func_name,
     callback=cb_name, body=body)

    def create_sig_for_func(real_func):
        func = block.compile(**{cb_name: real_func})[func_name]
        return backend.get_callback_object(func, sig_args)

    return create_sig_for_func


def generate_signal_callback(info):
    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break

    args = info.get_args()
    arg_types = [a.get_type() for a in args]

    cb_func = None
    try:
        cb_func = _generate_signal_callback(backend, info, args, arg_types)
    except NotImplementedError:
        pass

    if not cb_func:
        raise NotImplementedError

    return cb_func
