# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
from ctypes import cdll, c_void_p, cast, c_size_t


if os.name == "nt":
    _so_mapping = {
        "glib-2.0": "libglib-2.0-0.dll",
        "gobject-2.0": "libgobject-2.0-0.dll",
        "girepository-1.0": "libgirepository-1.0-1.dll",
    }
else:
    _so_mapping = {
        "glib-2.0": "libglib-2.0.so.0",
        "gobject-2.0": "libgobject-2.0.so.0",
        "girepository-1.0": "libgirepository-1.0.so.1",
    }


if os.name == "nt":
    stdlib = memcpy = cdll.msvcrt
else:
    stdlib = getattr(cdll, "libc.so.6")

memcpy = stdlib.memcpy
memcpy.argtypes = [c_void_p, c_void_p, c_size_t]
memcpy.restype = c_void_p

_internal = {}


def find_library(name, cached=True, internal=True):
    """
        cached: Return a new instance
        internal: return a shared instance that's not the ctypes cached one
    """

    # a new one
    if not cached:
        return cdll.LoadLibrary(_so_mapping[name])

    # from the shared internal set or a new one
    if internal:
        if name not in _internal:
            _internal[name] = cdll.LoadLibrary(_so_mapping[name])
        return _internal[name]

    # a shared one
    return getattr(cdll, _so_mapping[name])


class _CProperty(object):
    def __init__(self, *args):
        self.args = args

    def __get__(self, instance, owner):
        if instance is None:
            return self

        lib, name, symbol, ret, args = self.args
        func = getattr(lib, symbol)
        func.argtypes = args
        func.restype = ret

        value = func(instance)
        setattr(instance, name, value)
        return value


class _CMethod(object):
    def __init__(self, *args):
        self.args = args

    def __get__(self, instance, owner):
        lib, name, symbol, ret, args, wrap, unref = self.args
        func = getattr(lib, symbol)
        func.argtypes = args
        func.restype = ret

        def unref_func(*x):
            instance = func(*x)
            instance._unref = True
            return instance

        if wrap:
            if unref:
                setattr(owner, name, unref_func)
            else:
                setattr(owner, name, lambda *x: func(*x))
            return getattr(instance, name)
        else:
            # FIXME: handle unref
            setattr(owner, name, staticmethod(func))
            return getattr(owner, name)


def gicast(obj, type_):
    """cast and transfer ownership to the now object"""
    new_obj = cast(obj, type_)
    new_obj._unref = obj._unref
    obj._unref = False
    return new_obj


_wraps = []


def wrap_class(*args):
    global _wraps

    _wraps.append(args)


def wrap_setup():
    global _wraps

    wraps = _wraps
    for lib, base, ptr, prefix, methods in wraps:
        for method in methods:
            unref = False
            if len(method) == 3:
                name, ret, args = method
            else:
                name, ret, args, unref = method

            symbol = prefix + name
            is_method = args and args[0] == ptr
            if is_method:
                # Methods that have no arguments and return no pointer type
                # can be getters and the values can be cached. hurray!
                is_pointer = hasattr(ret, "contents") or ret is c_void_p
                is_void = ret is None
                if len(args) == 1 and not is_void and not is_pointer:
                    attr_name = name
                    if attr_name.startswith("get_"):
                        attr_name = attr_name[4:]
                    elif attr_name.startswith("to_"):
                        attr_name = attr_name[3:]
                    # e.g. conflict with ctypes "contents" attribute
                    if hasattr(ptr, attr_name):
                        attr_name += "_"
                    prop = _CProperty(lib, attr_name, symbol, ret, args)
                    setattr(ptr, attr_name, prop)
                else:
                    method = _CMethod(
                        lib, name, symbol, ret, args, True, unref)
                    setattr(ptr, name, method)
            else:
                static_method = _CMethod(
                    lib, name, symbol, ret, args, False, unref)
                setattr(base, name, static_method)

    _wraps = []
