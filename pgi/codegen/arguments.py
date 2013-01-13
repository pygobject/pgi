# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GIDirection, GIArrayType, GITypeTag


class Argument(object):
    """Base class for argument types

    is_aux -- if the arg is handled by another arg
    out_vars -- a list of variables to return
    call_var -- variable name passed to the function
    """

    TAG = None

    is_aux = False
    call_var = ""
    out_vars = []

    def __init__(self, info, type_, args, backend):
        super(Argument, self).__init__()

        self.args = args
        self.info = info
        self.name = info.get_name()
        self.type = type_
        self.backend = backend
        self.call_var = self.name

    def setup(self):
        pass

    def pre_call(self):
        pass

    def post_call(self):
        pass

    def is_pointer(self):
        return self.type.is_pointer()

    def is_direction_in(self):
        direction = self.info.get_direction().value
        return direction in (GIDirection.INOUT, GIDirection.IN)

    def is_direction_out(self):
        direction = self.info.get_direction().value
        return direction in (GIDirection.INOUT, GIDirection.OUT)

    def is_zero_terminated(self):
        return self.type.is_zero_terminated()

    def __repr__(self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class ArrayArgument(Argument):
    TAG = GITypeTag.ARRAY

    def setup(self):
        type_ = self.info.get_type()
        length_arg_index = type_.get_array_length()
        aux = self.args[length_arg_index]
        aux.is_aux = True
        self._aux = aux
        self._array_type = self.type.get_array_type().value

    def pre_call(self):
        backend = self.backend
        array_type = self._array_type

        if array_type == GIArrayType.C:
            if self.is_direction_in() and self.is_direction_out():
                if not self.is_zero_terminated() and self.is_pointer():
                    block, data, data_ref, length, lref = \
                        backend.pack_array_ptr_fixed_c(self.name)
                    self.call_var = data_ref
                    self._aux.call_var = lref
                    return block
        elif array_type == GIArrayType.ARRAY:
            pass
        elif array_type == GIArrayType.PTR_ARRAY:
            pass
        elif array_type == GIArrayType.BYTE_ARRAY:
            pass

    def post_call(self):
        pass


class InterfaceArgument(Argument):
    TAG = GITypeTag.INTERFACE

    def pre_call(self):
        block, var = self.backend.pack_interface(self.name)
        self.call_var = var
        return block


class Int32Argument(Argument):
    TAG = GITypeTag.INT32


class Utf8Argument(Argument):
    TAG = GITypeTag.UTF8


_classes = {}


def _find_arguments():
    global _classes
    cls = [a for a in globals().values() if isinstance(a, type)]
    args = [a for a in cls if issubclass(a, Argument) and a is not Argument]
    _classes = dict(((a.TAG, a) for a in args))
_find_arguments()


def get_argument_class(arg_type):
    global _classes
    tag_value = arg_type.get_tag().value
    return _classes.get(tag_value, Argument)
