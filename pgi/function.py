# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes
from ctypes import cast

from pgi.gir import GIFunctionInfoPtr, GITypeTag, GIDirection
from pgi.util import typeinfo_to_ctypes


def indent(lines):
    return ["    " + l for l in lines]


def wrap_exc(lines, catch, new, arg):
    l = []
    l.append("try:")
    l.extend(indent(lines))
    l.append("except %s:" % catch)
    l.extend(indent(["raise %s('%s')" % (new, arg)]))
    return l


def wrap_func(name, args, lines):
    l = ["def %s(%s):" % (name, ", ".join(args))]
    l.extend(indent(lines))
    return l


def unpack_array_zeroterm(name):
    l = ["temp2 = []"]
    l.append("i = 0")
    l.append("x = %s and %s[i]" % (name, name))
    l.append("while x:")

    loop = ["temp2.append(x)",
            "i += 1",
            "x = %s[i]" % name]

    l.extend(indent(loop))
    l.append("%s = temp2" % name)
    return l


def call_func(name, args, res):
    return "%s = %s(%s)" % (res, name, ", ".join(args))


def return_var(name):
    return "return %s" % name


def FunctionAttribute(info, namespace, name, lib):
    func_info = cast(info, GIFunctionInfoPtr)
    args = func_info.get_args()

    symbol = func_info.get_symbol()
    h = getattr(lib, symbol)

    arguments = []
    for arg in args:
        if arg.get_direction().value == GIDirection.OUT:
            continue
        arguments.append(arg)

    return_type = func_info.get_return_type()
    h.restype = typeinfo_to_ctypes(return_type)
    h.argtypes = [typeinfo_to_ctypes(a.get_type()) for a in arguments]

    lines = []
    arg_names = [a.get_name() for a in arguments]
    lines.append(call_func("handle", arg_names, "temp"))
    lines = wrap_exc(lines, "ctypes.ArgumentError",
                     "TypeError", "Wrong input type")

    if return_type.get_tag().value == GITypeTag.ARRAY:
        if return_type.is_zero_terminated():
            lines.extend(unpack_array_zeroterm("temp"))

    if h.restype:
        lines.append(return_var("temp"))
    f = "\n".join(wrap_func(name, arg_names, lines))

    code = compile(f, "<%s>" % namespace, "exec")
    d = {"handle": h, "ctypes": ctypes}
    exec code in d

    func = d[name]
    func._is_function = True
    return func
