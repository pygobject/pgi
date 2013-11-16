# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.


class ForeignStruct(object):

    def from_pointer(self, pointer):
        raise NotImplementedError

    def to_pointer(self, instance):
        raise NotImplementedError

    def destroy(self, pointer):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError


def _get_foreign(namespace, name):
    if namespace != "cairo":
        return

    try:
        import cffi
        import cairocffi
    except ImportError:
        return

    # check for a cairocffi that supports cffi 0.6
    if isinstance(cairocffi.FORMAT_ARGB32, str):
        return

    ffi = cffi.FFI()

    if namespace == "cairo" and name == "Context":
        class Context(ForeignStruct):
            def from_pointer(self, pointer):
                pointer = ffi.cast("void*", pointer)
                return cairocffi.Context._from_pointer(pointer, True)

            def to_pointer(self, instance):
                return instance._pointer

            def get_type(self):
                return cairocffi.Context

        return Context()
    else:
        return


def get_foreign(namespace, name, _cache={}):
    key = (namespace, name)
    if key not in _cache:
        _cache[key] = _get_foreign(namespace, name)
    return _cache[key]
