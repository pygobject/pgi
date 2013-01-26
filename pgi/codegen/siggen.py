# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen import ACTIVE_BACKENDS
from pgi.codegen.utils import CodeBlock
from pgi.gir import GITypeTag, GIInfoType
from pgi.util import escape_name, escape_builtin, import_attribute


class SignalArgument(object):
    TAG = None

    is_aux = False

    def __init__(self, backend, info, type_, name):
        self.info = info
        self.name = name
        self.backend = backend
        self.type = type_

    def setup(self):
        pass

    def process(self):
        return None, self.name


class InterfaceArgument(SignalArgument):
    TAG = GITypeTag.INTERFACE

    def process(self):
        backend = self.backend
        iface = self.type.get_interface()
        iface_type = iface.type.value
        iface_namespace = iface.namespace
        iface_name = iface.name
        iface.unref()

        if iface_type == GIInfoType.OBJECT:
            return backend.unpack_object(self.name)
        elif iface_type == GIInfoType.UNION:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_union(self.name, attr)
        elif iface_type == GIInfoType.STRUCT:
            attr = import_attribute(iface_namespace, iface_name)
            return backend.unpack_struct(self.name, attr)

        raise NotImplementedError("interface %r not supported")


_classes = {}
def _find_signals():
    global _classes
    for var in globals().values():
        if not isinstance(var, type):
            continue
        if issubclass(var, SignalArgument) and var is not SignalArgument:
            _classes[var.TAG] = var
_find_signals()


def get_signal_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    try:
        return _classes[tag_value]
    except KeyError:
        raise NotImplementedError("%r signal argument not implemented" % arg_type.tag)


def _generate_signal_callback(backend, info, args, arg_types, callback):
    sig_args = []

    for arg, type_ in zip(args, arg_types):
        cls = get_signal_class(type_)
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

    block, var = backend.parse("""
def $cb_wrapper($args):
    $body
    $ret = $callback($out_args)
    # FIXME: convert return value
""", args=argument_list, out_args=forward_arguments, cb_wrapper=func_name,
     callback=callback, body=body)

    func = block.compile()[func_name]
    return backend.get_callback_object(func, sig_args)


def generate_signal_callback(info, callback):
    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break

    args = info.get_args()
    arg_types = [a.get_type() for a in args]

    cb_func = None
    try:
        cb_func = _generate_signal_callback(backend, info, args,
                                            arg_types, callback)
    except NotImplementedError:
        pass

    for arg in args:
        arg.unref()
    for type_ in arg_types:
        type_.unref()

    if not cb_func:
        raise NotImplementedError

    return cb_func
