# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cdll


_so_mapping = {
    "glib-2.0": "libglib-2.0.so.0",
    "gobject-2.0": "libgobject-2.0.so.0",
    "girepository-1.0": "libgirepository-1.0.so.1",
}

find_library = lambda name: getattr(cdll, _so_mapping[name])


class _CMethod(object):
    def __init__(self, *args):
        self.args = args

    def __get__(self, instance, owner):
        lib, name, prefix, ret, args, wrap = self.args
        func = getattr(lib, prefix + name)
        func.argtypes = args
        func.restype = ret

        if wrap:
            setattr(owner, name, lambda *x: func(*x))
            return getattr(instance, name)
        setattr(owner, name, func)
        return func


_wraps = []


def wrap_class(*args):
    global _wraps

    _wraps.append(args)


def wrap_setup():
    global _wraps

    wraps = _wraps
    for (lib, base, ptr, pre, methods) in wraps:
        for name, ret, args in methods:
            if args and args[0] == ptr:
                setattr(ptr, name, _CMethod(lib, name, pre, ret, args, True))
            else:
                setattr(base, name, _CMethod(lib, name, pre, ret, args, False))

    _wraps = []
