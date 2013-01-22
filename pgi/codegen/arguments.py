# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GIDirection, GIArrayType, GITypeTag, GIInfoType
from pgi.util import import_attribute


class Argument(object):
    """Base class for argument types

    is_aux   -- if the arg is handled by another arg
    in_var   -- variable name in the function def
    out_var  -- variable name to return
    call_var -- variable name passed to the function
    """

    TAG = None

    is_aux = False
    in_var = ""
    call_var = ""
    out_var = ""

    def __init__(self, arguments, backend):
        self.args = arguments
        self.backend = backend

    def setup(self):
        pass

    def pre_call(self):
        pass

    def post_call(self):
        pass


class ErrorArgument(Argument):

    def pre_call(self):
        block, error, ref = self.backend.setup_gerror()
        self.call_var = ref
        self._error = error
        return block

    def post_call(self):
        return self.backend.check_gerror(self._error)


class GIArgument(Argument):

    def __init__(self, name, arguments, backend, info, type_):
        Argument.__init__(self, arguments, backend)

        self.info = info
        self.name = name
        self.type = type_
        self.call_var = name
        self.direction = self.info.direction.value

        if self.is_direction_in():
            self.in_var = name

    def may_be_null(self):
        return self.info.may_be_null

    def is_pointer(self):
        return self.type.is_pointer

    def is_direction_in(self):
        return self.direction in (GIDirection.INOUT, GIDirection.IN)

    def is_direction_out(self):
        return self.direction in (GIDirection.INOUT, GIDirection.OUT)

    def is_direction_inout(self):
        return self.direction == GIDirection.INOUT

    def __repr__(self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class ArrayArgument(GIArgument):
    TAG = GITypeTag.ARRAY

    def setup(self):
        type_ = self.info.get_type()

        # mark other arg as aux so we handle it alone
        aux = self.args[type_.array_length]
        aux.is_aux = True
        self._aux = aux

        self._array_type = self.type.array_type.value
        self._param_type = self.type.get_param_type(0).tag.value

    def is_zero_terminated(self):
        return self.type.is_zero_terminated

    def _pre_c(self):
        backend = self.backend

        if self.is_direction_inout():
            if not self.is_zero_terminated():
                block, data, data_ref, length, lref = \
                    backend.pack_array_ptr_fixed_c_in_out(self.name)
                self.call_var = data_ref
                self._aux.call_var = lref
                # vars for out
                self._data = data
                self._length = length
                return block
        elif self.is_direction_in():
            if not self.is_zero_terminated():
                block, data_ref, length = \
                    backend.pack_array_ptr_fixed_c_in(self.name)
                self.call_var = data_ref
                self._aux.call_var = length
                return block

    def pre_call(self):
        array_type = self._array_type

        if array_type == GIArrayType.C:
            return self._pre_c()
        elif array_type == GIArrayType.ARRAY:
            pass
        elif array_type == GIArrayType.PTR_ARRAY:
            pass
        elif array_type == GIArrayType.BYTE_ARRAY:
            pass

    def _post_c(self):
        b = self.backend
        if self.is_direction_out():
            if not self.is_zero_terminated() and self.is_pointer():
                block, out = b.unpack_array_ptr_fixed_c(self._data, self._length)
                self.out_var = out
                return block

    def post_call(self):
        array_type = self._array_type

        if array_type == GIArrayType.C:
            return self._post_c()


class InterfaceArgument(GIArgument):
    TAG = GITypeTag.INTERFACE

    def _pre_object(self):
        if self.may_be_null():
            block, var = self.backend.pack_object_null(self.name)
        else:
            block, var = self.backend.pack_object(self.name)
        self.call_var = var
        return block

    def _pre_struct(self, namespace, name):
        if self.is_direction_in():
            block, var = self.backend.pack_struct(self.name)
            self.call_var = var
            return block
        else:
            type_ = import_attribute(namespace, name)
            block, data, ref = self.backend.setup_struct(self.name, type_)
            self.call_var = ref
            self.out_var = data
            return block

    def pre_call(self):
        iface = self.type.get_interface()
        iface_name = iface.name
        iface_namespace = iface.namespace
        iface_type = iface.type.value
        iface.unref()

        if iface_type == GIInfoType.OBJECT:
            return self._pre_object()
        elif iface_type == GIInfoType.ENUM:
            return
        elif iface_type == GIInfoType.STRUCT:
            return self._pre_struct(iface_namespace, iface_name)


class BoolArgument(GIArgument):
    TAG = GITypeTag.BOOLEAN

    def pre_call(self):
        block, var = self.backend.pack_bool(self.name)
        self.call_var = var
        return block


class UInt8Argument(GIArgument):
    TAG = GITypeTag.UINT8


class VoidArgument(GIArgument):
    TAG = GITypeTag.VOID


class Int32Argument(GIArgument):
    TAG = GITypeTag.INT32


class Int64Argument(GIArgument):
    TAG = GITypeTag.INT64


class UINT32Argument(GIArgument):
    TAG = GITypeTag.UINT32

    def pre_call(self):
        if self.is_direction_out():
            block, data, ref = self.backend.pack_uint32_ptr()
            self._data = data
            self.call_var = ref
            return block
        else:
            block, out = self.backend.pack_uint32(self.name)
            self.call_var = out
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_basic(self._data)
            self.out_var = var
            return block


class Utf8Argument(GIArgument):
    TAG = GITypeTag.UTF8

    def pre_call(self):
        if self.may_be_null():
            block, var = self.backend.pack_string_null(self.name)
        else:
            block, var = self.backend.pack_string(self.name)
        self.call_var = var
        return block


class FloatArgument(GIArgument):
    TAG = GITypeTag.FLOAT

    def pre_call(self):
        if self.is_direction_out():
            block, data, ref = self.backend.setup_float_ptr()
            self._data = data
            self.call_var = ref
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_basic(self._data)
            self.out_var = var
            return block


class DoubleArgument(GIArgument):
    TAG = GITypeTag.DOUBLE

    def pre_call(self):
        if self.is_direction_out():
            block, data, ref = self.backend.setup_double_ptr()
            self._data = data
            self.call_var = ref
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_basic(self._data)
            self.out_var = var
            return block


class GTypeArgument(GIArgument):
    TAG = GITypeTag.GTYPE

    def pre_call(self):
        block, out = self.backend.pack_gtype(self.name)
        self.call_var = out
        return block


_classes = {}


def _find_arguments():
    global _classes
    cls = [a for a in globals().values() if isinstance(a, type)]
    args = [a for a in cls if issubclass(a, GIArgument) and a is not GIArgument]
    _classes = dict(((a.TAG, a) for a in args))
_find_arguments()


def get_argument_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    return _classes[tag_value]
