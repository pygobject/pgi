# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GIDirection, GIArrayType, GITypeTag, GIInfoType, GITransfer
from pgi.gir import GICallableInfoPtr
from pgi.util import import_attribute
from pgi.ctypesutil import gicast
from pgi.gtype import PGType


class Argument(object):
    """Base class for argument types

    is_aux   -- if the arg is handled by another arg
    in_var   -- variable name in the function def
    out_var  -- variable name to return
    call_var -- variable name passed to the function
    py_type  -- a python type for docs / possibly annotation
    """

    is_aux = False
    in_var = ""
    call_var = ""
    out_var = ""
    py_type = None

    def __init__(self, arguments, backend):
        self.args = arguments
        self.backend = backend

    @classmethod
    def get_class(cls, type_):
        return cls

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

    TAG = None

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

    def transfer_nothing(self):
        return self.info.ownership_transfer.value == GITransfer.NOTHING

    def transfer_container(self):
        return self.info.ownership_transfer.value == GITransfer.CONTAINER

    def transfer_everything(self):
        return self.info.ownership_transfer.value == GITransfer.EVERYTHING

    def __repr__(self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class ArrayArgument(GIArgument):
    TAG = GITypeTag.ARRAY
    py_type = list

    @classmethod
    def get_class(cls, type_):
        type_ = type_.array_type.value

        if type_ == GIArrayType.C:
            return CArrayArgument

        raise NotImplementedError("unsupported array type")

    def is_zero_terminated(self):
        return self.type.is_zero_terminated


class CArrayArgument(ArrayArgument):

    def setup(self):
        # mark other arg as aux so we handle it alone
        if self.array_length != -1:
            aux = self.args[self.array_length]
            aux.is_aux = True
            self._aux = aux

        self._param_type = self.type.get_param_type(0)

    @property
    def array_length(self):
        return self.type.array_length

    @property
    def array_fixed_size(self):
        return self.type.array_fixed_size

    def _pack_param(self, type_):
        # HACK: reuse argument classes of subtypes for packing
        # ...replace with something sane

        class SubInfo(object):
            @property
            def direction(self):
                class X(object):
                    value = GIDirection.IN
                return X()

            @property
            def ownership_transfer(self):
                class X(object):
                    value = GITransfer.EVERYTHING
                return X()

            @property
            def may_be_null(self):
                return False

        param_cls = get_argument_class(type_)
        in_name = self.backend._var()
        sub_arg = param_cls(in_name, [], self.backend, SubInfo(), type_)
        sub_arg.setup()
        block = sub_arg.pre_call()
        return block, in_name, sub_arg.call_var

    def pre_call(self):
        backend = self.backend

        if self.is_direction_inout():
            param_block, in_var, out_var = self._pack_param(self._param_type)

            if not self.is_zero_terminated():
                if self.array_length != -1:
                    length_type = self._aux.type

                    block, data, length = backend.pack_carray_basic_length(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length_type)

                    block2, self._aux.call_var = backend.get_reference(length)
                    block2.write_into(block)
                else:
                    length = str(self.array_fixed_size)

                    block, data = backend.pack_carray_basic_fixed(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length)

                block2, self.call_var = backend.get_reference(data)
                block2.write_into(block)

                self._data = data
                self._length = length

                return block

            raise NotImplementedError

        elif self.is_direction_in():
            param_block, in_var, out_var = self._pack_param(self._param_type)

            if self.array_length != -1:
                length_type = self._aux.type

                if self.is_zero_terminated():
                    block, data, length = backend.pack_carray_basic_length_zero(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length_type)
                else:
                    block, data, length = backend.pack_carray_basic_length(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length_type)

                self._aux.call_var = length
                self.call_var = data
    
                return block
            else:
                length = str(self.array_fixed_size)

                if self.is_zero_terminated():
                    block, data = backend.pack_carray_basic_fixed_zero(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length)
                else:
                    block, data = backend.pack_carray_basic_fixed(
                        self.name, in_var, out_var, param_block,
                        self._param_type, length)

                self.call_var = data
                return block

        else:
            if not self.is_zero_terminated():
                if self.array_length == -1:
                    length = str(self.array_fixed_size)
                    block, data, ptr = backend.setup_carray_basic_fixed(length, self._param_type)
                    self._data = ptr
                    block2, self.call_var = backend.get_reference(ptr)
                    block2.write_into(block)
                    self.call_var = ptr
                    return block
                else:
                    length_type = self._aux.type

                    block, data, ptr, length = backend.setup_carray_basic_length(self._param_type, length_type)
                    self.call_var = ptr
                    block2, self._aux.call_var = backend.get_reference(length)
                    block2.write_into(block)
                    self._length = length
                    self._data = data
                    return block
            else:
                raise NotImplementedError("zero")

    def post_call(self):
        if not self.is_direction_out():
            return

        if not self.is_zero_terminated():
            block, data = self.backend.deref_pointer(self._data)

            if self.array_length == -1:
                length = str(self.array_fixed_size)
                block2, out = self.backend.unpack_carray_basic_fixed(data, length)
                block2.write_into(block)
            else:
                block2, out = self.backend.unpack_carray_basic_length(data, self._length)
                block2.write_into(block)

            self.out_var = out
            return block

        raise NotImplementedError("post zero")


class InterfaceArgument(GIArgument):
    TAG = GITypeTag.INTERFACE
    py_type = object

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.OBJECT:
            return ObjectArgument
        elif iface_type == GIInfoType.ENUM:
            return EnumArgument
        elif iface_type == GIInfoType.STRUCT:
            return StructArgument
        elif iface_type == GIInfoType.CALLBACK:
            return CallbackArgument

        raise NotImplementedError("Unsupported interface type %r" % iface.type)


class CallbackArgument(InterfaceArgument):
    py_type = type(lambda: None)

    def pre_call(self):
        iface = self.type.get_interface()
        iface = gicast(iface, GICallableInfoPtr)

        from pgi.codegen.siggen import generate_callback
        pack = generate_callback(iface)
        block, out = self.backend.pack_callback(self.name, pack)
        self.call_var = out
        return block


class EnumArgument(InterfaceArgument):
    pass


class StructArgument(InterfaceArgument):

    def pre_call(self):
        iface = self.type.get_interface()
        iface_name = iface.name
        iface_namespace = iface.namespace

        if self.is_direction_in():
            block, var = self.backend.pack_struct(self.name)
            self.call_var = var
            return block
        else:
            type_ = import_attribute(iface_namespace, iface_name)
            block, data, ref = self.backend.setup_struct(self.name, type_)
            self.call_var = ref
            self.out_var = data
            return block


class ObjectArgument(InterfaceArgument):

    def pre_call(self):
        if self.is_direction_in():
            if self.may_be_null():
                block, self._data = self.backend.pack_object_null(self.name)
            else:
                block, self._data = self.backend.pack_object(self.name)

            if self.transfer_everything():
                block2 = self.backend.ref_object_null(self.name)
                block2.write_into(block)

            if self.is_direction_out():
                block2, self.call_var = self.backend.get_reference(self._data)
                block2.write_into(block)
            else:
                self.call_var = self._data

            return block
        else:
            block, self._data = self.backend.setup_pointer()
            block2, self.call_var = self.backend.get_reference(self._data)
            block2.write_into(block)
            return block

    def post_call(self):
        if self.is_direction_out():
            block, out = self.backend.unpack_basic(self._data)
            block2, out = self.backend.unpack_object(out)
            block2.write_into(block)
            if self.transfer_nothing():
                block2 = self.backend.ref_object_null(out)
                block2.write_into(block)
            self.out_var = out
            return block


class BasicTypeArgument(GIArgument):
    TYPE_NAME = ""

    def pre_call(self):
        if self.is_direction_inout():
            pack = getattr(self.backend, "pack_%s" % self.TYPE_NAME)
            block, self._data = pack(self.name)
            block2, self.call_var = self.backend.get_reference(self._data)
            block2.write_into(block)
            return block
        elif self.is_direction_in():
            pack = getattr(self.backend, "pack_%s" % self.TYPE_NAME)
            block, var = pack(self.name)
            self.call_var = var
            return block
        else:
            setup = getattr(self.backend, "setup_%s" % self.TYPE_NAME)
            block, self._data = setup()
            block2, self.call_var = self.backend.get_reference(self._data)
            block2.write_into(block)
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_basic(self._data)
            self.out_var = var
            return block


class BoolArgument(BasicTypeArgument):
    TAG = GITypeTag.BOOLEAN
    TYPE_NAME = "bool"
    py_type = bool


class Int8Argument(BasicTypeArgument):
    TAG = GITypeTag.INT8
    TYPE_NAME = "int8"
    py_type = int


class UInt8Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT8
    TYPE_NAME = "uint8"
    py_type = int


class Int16Argument(BasicTypeArgument):
    TAG = GITypeTag.INT16
    TYPE_NAME = "int16"
    py_type = int


class UInt16Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT16
    TYPE_NAME = "uint16"
    py_type = int


class Int32Argument(BasicTypeArgument):
    TAG = GITypeTag.INT32
    TYPE_NAME = "int32"
    py_type = int


class Int64Argument(BasicTypeArgument):
    TAG = GITypeTag.INT64
    TYPE_NAME = "int64"
    py_type = int


class UInt64Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT64
    TYPE_NAME = "uint64"
    py_type = int


class UINT32Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT32
    TYPE_NAME = "uint32"
    py_type = int


class FloatArgument(BasicTypeArgument):
    TAG = GITypeTag.FLOAT
    TYPE_NAME = "float"
    py_type = float


class DoubleArgument(BasicTypeArgument):
    TAG = GITypeTag.DOUBLE
    TYPE_NAME = "double"
    py_type = float


class VoidArgument(GIArgument):
    TAG = GITypeTag.VOID

    def setup(self):
        if self.is_pointer():
            self.py_type = int

    def pre_call(self):
        if self.is_pointer():
            if not self.may_be_null():
                block, out = self.backend.pack_pointer(self.name)
                self.call_var = out
                return block

        raise NotImplementedError


class Utf8Argument(GIArgument):
    TAG = GITypeTag.UTF8
    py_type = str

    def pre_call(self):
        if self.is_direction_inout():
            block, data = self.backend.pack_utf8(self.name)
            if self.transfer_everything():
                block3, data = self.backend.dup_string(data)
                block3.write_into(block)
            block2, ref = self.backend.get_reference(data)
            block2.write_into(block)
            self.call_var = ref
            self._data = data
            return block
        elif self.is_direction_in():
            if self.may_be_null():
                block, var = self.backend.pack_utf8_null(self.name)
            else:
                block, var = self.backend.pack_utf8(self.name)
            self.call_var = var
            return block
        elif self.is_direction_out():
            block, data = self.backend.setup_string()
            block2, ref = self.backend.get_reference(data)
            block2.write_into(block)
            self.call_var = ref
            self._data = data
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_utf8(self._data)
            if self.transfer_everything():
                block2 = self.backend.free_pointer(self._data)
                block2.write_into(block)
            self.out_var = var
            return block


class GTypeArgument(GIArgument):
    TAG = GITypeTag.GTYPE
    py_type = PGType

    def pre_call(self):
        if self.is_direction_inout():
            block, self._data = self.backend.pack_gtype(self.name)
            block2, self.call_var = self.backend.get_reference(self._data)
            block2.write_into(block)
            return block
        elif self.is_direction_in():
            block, var = self.backend.pack_gtype(self.name)
            self.call_var = var
            return block
        else:
            block, self._data = self.backend.setup_gtype()
            block2, self.call_var = self.backend.get_reference(self._data)
            block2.write_into(block)
            return block

    def post_call(self):
        if self.is_direction_out():
            block, var = self.backend.unpack_gtype(self._data)
            self.out_var = var
            return block


_classes = {}


def _find_arguments():
    global _classes
    for var in globals().values():
        if not isinstance(var, type):
            continue
        if issubclass(var, GIArgument) and var is not GIArgument:
            _classes[var.TAG] = var
_find_arguments()


def get_argument_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    try:
        cls = _classes[tag_value]
    except KeyError:
        raise NotImplementedError("%r argument not implemented" % arg_type.tag)
    else:
        return cls.get_class(arg_type)
