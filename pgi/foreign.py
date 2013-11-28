# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Foreign structs make it possible for gi to interact with other python
libraries. For example it allows functions to take cairo structs created
with cairocffi.
"""


class ForeignStruct(object):
    """The foreign struct interface"""

    def from_pointer(self, pointer):
        raise NotImplementedError

    def to_pointer(self, instance):
        raise NotImplementedError

    def destroy(self, pointer):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError


class ForeignError(Exception):
    pass


def _get_foreign(namespace, name):
    """Returns a ForeignStruct implementation or raises ForeignError"""

    if namespace != "cairo":
        raise ForeignError("Foreign %r structs not supported" % namespace)

    try:
        import cffi
        import cairocffi
    except ImportError:
        raise ForeignError(
            "Support for foreign cairo struct needs cffi and cairocffi")

    # check for a cairocffi that supports cffi 0.6
    if isinstance(cairocffi.FORMAT_ARGB32, str):
        raise ForeignError("Too old cairocffi")

    ffi = cffi.FFI()

    if name == "Context":

        class Context(ForeignStruct):
            def from_pointer(self, pointer):
                pointer = ffi.cast("void*", pointer)
                return cairocffi.Context._from_pointer(pointer, True)

            def to_pointer(self, instance):
                return int(ffi.cast("intptr_t", instance._pointer))

            def get_type(self):
                return cairocffi.Context

        return Context()
    elif name == "Surface":

        class Surface(ForeignStruct):
            def from_pointer(self, pointer):
                pointer = ffi.cast("void*", pointer)
                return cairocffi.Surface._from_pointer(pointer, True)

            def to_pointer(self, instance):
                return int(ffi.cast("intptr_t", instance._pointer))

            def get_type(self):
                return cairocffi.Surface

        return Surface()
    else:
        raise ForeignError("cairo struct %r not supported" % name)


def check_foreign(namespace, name):
    """Raises ValueError if the specified foreign struct isn't supported or
    the needed dependencies aren't installed.

    e.g.: check_foreign('cairo', 'Context')
    """

    try:
        _get_foreign(namespace, name)
    except ForeignError as e:
        raise ValueError(e)


_FOREIGN = {}
"""Cache for ForeignStruct instances"""


def get_foreign(namespace, name):
    """Returns a ForeignStruct implementation or None.

    e.g.: get_foreign('cairo', 'Context')
    """

    global _FOREIGN

    key = (namespace, name)
    if key not in _FOREIGN:
        try:
            foreign = _get_foreign(namespace, name)
        except ForeignError:
            foreign = None
        _FOREIGN[key] = foreign

    return _FOREIGN[key]
