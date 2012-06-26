# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

_dll_cache = {}
_so_mapping = {
    "glib-2.0": "libglib-2.0.so.0",
    "gobject-2.0": "libgobject-2.0.so.0",
    "girepository-1.0": "libgirepository-1.0.so.1",
}


def load(name):
    global _dll_cache, _so_mapping
    if name not in _dll_cache:
        from ctypes import CDLL
        _dll_cache[name] = CDLL(_so_mapping[name])
    return _dll_cache[name]

count = 0


def _debug(f, name, base):
    def _add(*args):
        global count
        count += 1
        print count, base.__name__ + "." + name
        return f(*args)
    return _add


def wrap_class(lib, base, ptr, prefix, methods):
    for name, ret, args in methods:
        func = getattr(lib, prefix + name)
        func.argtypes = args
        func.restype = ret

        if args and args[0] == ptr:
            add_self = lambda f: lambda *args: f(*args)
            setattr(ptr, name, add_self(func))
            #setattr(ptr, name, _debug(func, name, base))
        else:
            setattr(base, name, func)
