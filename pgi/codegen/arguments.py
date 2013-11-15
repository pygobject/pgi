# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib.gir import GIDirection, GIArrayType, GITypeTag, GIInfoType
from pgi.clib.gir import GITransfer
from pgi.clib.gobject import GCallback
from pgi.gtype import PGType
from pgi.gerror import PGError


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

    class FakeType(object):
        class Y(object):
            value = GITypeTag.ERROR
        tag = Y()

    def pre_call(self):
        var = self.backend.get_type(ErrorArgument.FakeType(), True)

        self._error = var.new()
        self.call_var = var.get_reference(self._error)
        return var.block

    def post_call(self):
        var = self.backend.get_type(ErrorArgument.FakeType(), True)

        out = var.unpack(self._error)
        var.free(self._error)
        var.check_raise(out)
        return var.block


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

    def get_type(self):
        return self.backend.get_type(self.type, self.info.may_be_null)

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

    def is_caller_allocates(self):
        return self.info.is_caller_allocates

    def __repr__(self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class GIErrorArgument(GIArgument):
    TAG = GITypeTag.ERROR
    py_type = PGError

    def pre_call(self):
        var = self.get_type()
        if self.is_direction_out():
            self._error = var.new()
            self.call_var = var.get_reference(self._error)
            return var.block

        raise NotImplementedError("Error not out")

    def post_call(self):
        if not self.is_direction_out():
            return

        var = self.get_type()
        self.out_var = var.unpack(self._error)
        if self.transfer_everything():
            var.free(self._error)

        return var.block


class ArrayArgument(GIArgument):
    TAG = GITypeTag.ARRAY
    py_type = list

    @classmethod
    def get_class(cls, type_):
        type_ = type_.array_type.value

        if type_ == GIArrayType.C:
            return CArrayArgument

        raise NotImplementedError("unsupported array type")


class CArrayArgument(ArrayArgument):

    def setup(self):
        # mark other arg as aux so we handle it alone
        if self.type.array_length != -1:
            aux = self.args[self.type.array_length]
            aux.is_aux = True
            self._aux = aux

    def pre_call(self):
        var = self.get_type()
        if self.is_direction_inout():
            checked = var.check(self.name)
            if self.type.array_length != -1:
                self._data, self._length = var.pack(checked, self._aux.type)
                self._aux.call_var = var.get_reference(self._length)
            else:
                self._data, length = var.pack(checked, None)
            self.call_var = var.get_reference(self._data)
            return var.block
        elif self.is_direction_in():
            checked = var.check(self.name)
            if self.type.array_length != -1:
                self.call_var, length = var.pack(checked, self._aux.type)
                self._aux.call_var = length
            else:
                self.call_var, dummy = var.pack(checked, None)
            return var.block
        else:
            if self.type.array_length != -1:
                self._data, self._length = var.new(self._aux.type)
                self._aux.call_var = var.get_reference(self._length)
            else:
                self._data, dummy = var.new(None)
            self.call_var = var.get_reference(self._data)
            return var.block

    def post_call(self):
        if not self.is_direction_out():
            return

        var = self.get_type()
        if self.type.array_length != -1:
            self.out_var = var.unpack(self._data, self._length)
        else:
            self.out_var = var.unpack(self._data, None)
        return var.block


class BaseInterfaceArgument(GIArgument):
    TAG = GITypeTag.INTERFACE
    py_type = object

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.OBJECT:
            return ObjectArgument
        elif iface_type == GIInfoType.INTERFACE:
            return ObjectArgument
        elif iface_type == GIInfoType.ENUM or iface_type == GIInfoType.FLAGS:
            return EnumFlagsArgument
        elif iface_type == GIInfoType.STRUCT:
            return StructArgument
        elif iface_type == GIInfoType.CALLBACK:
            return CallbackArgument

        raise NotImplementedError("Unsupported interface type %r" % iface.type)


class CallbackArgument(BaseInterfaceArgument):
    py_type = type(lambda: None)

    def setup(self):
        self._user_data = None
        if self.info.closure != -1:
            self._user_data = self.args[self.info.closure]
            self._user_data.is_aux = True

        self._destroy = None
        if self.info.destroy != -1:
            self._destroy = self.args[self.info.destroy]
            self._destroy.is_aux = True

    def pre_call(self):
        var = self.get_type()
        self.call_var = var.pack(var.check(self.name))

        if self._destroy:
            var.block.add_dependency("GCallback", GCallback)
            self._destroy.call_var = "GCallback()"

        if self._user_data:
            self._user_data.call_var = "None"

        return var.block


class EnumFlagsArgument(BaseInterfaceArgument):

    def pre_call(self):
        var = self.get_type()

        if self.is_direction_inout():
            self._data = var.pack(var.check(self.name))
            self.call_var = var.get_reference(self._data)
        elif self.is_direction_in():
            self.call_var = var.pack(var.check(self.name))
        else:
            self._data = var.new()
            self.call_var = var.get_reference(self._data)

        return var.block

    def post_call(self):
        if not self.is_direction_out():
            return

        var = self.get_type()
        self.out_var = var.unpack(var.pre_unpack(self._data))
        return var.block


class StructArgument(BaseInterfaceArgument):

    def pre_call(self):
        var = self.get_type()

        if self.is_direction_inout():
            self._data = var.pack(var.check(self.name))
            self.call_var = var.get_reference(self._data)
        elif self.is_direction_in():
            self.call_var = var.pack(var.check(self.name))
        else:
            if self.is_caller_allocates():
                self.call_var = self._data = var.alloc()
            else:
                self._data = var.new()
                self.call_var = var.get_reference(self._data)

        return var.block

    def post_call(self):
        if not self.is_direction_out():
            return

        var = self.get_type()
        self.out_var = var.unpack(var.pre_unpack(self._data))
        return var.block


class ObjectArgument(BaseInterfaceArgument):

    def pre_call(self):
        var = self.get_type()

        if self.is_direction_in():
            self._data = var.pack(var.check(self.name))

            if self.transfer_everything():
                var.ref(self.name)

            if self.is_direction_out():
                self.call_var = var.get_reference(self._data)
            else:
                self.call_var = self._data

            return var.block
        else:
            self._data = var.new()
            self.call_var = var.get_reference(self._data)

            return var.block

    def post_call(self):
        if self.is_direction_out():
            var = self.get_type()
            out = var.unpack(self._data)
            if self.transfer_nothing():
                var.ref(out)
            self.out_var = out
            return var.block


class BasicTypeArgument(GIArgument):
    TYPE_NAME = ""

    def pre_call(self):
        var = self.get_type()

        if self.is_direction_inout():
            self._data = var.pack(var.check(self.name))
            self.call_var = var.get_reference(self._data)
            return var.block
        elif self.is_direction_in():
            self.call_var = var.pack_in(var.check(self.name))
            return var.block
        else:
            self._data = var.new()
            self.call_var = var.get_reference(self._data)
            return var.block

    def post_call(self):
        if self.is_direction_out():
            var = self.get_type()
            self.out_var = var.unpack(var.pre_unpack(self._data))
            return var.block


class BoolArgument(BasicTypeArgument):
    TAG = GITypeTag.BOOLEAN
    py_type = bool


class Int8Argument(BasicTypeArgument):
    TAG = GITypeTag.INT8
    py_type = int


class UInt8Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT8
    py_type = int


class Int16Argument(BasicTypeArgument):
    TAG = GITypeTag.INT16
    py_type = int


class UInt16Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT16
    py_type = int


class Int32Argument(BasicTypeArgument):
    TAG = GITypeTag.INT32
    py_type = int


class Int64Argument(BasicTypeArgument):
    TAG = GITypeTag.INT64
    py_type = int


class UInt64Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT64
    py_type = int


class UINT32Argument(BasicTypeArgument):
    TAG = GITypeTag.UINT32
    py_type = int


class FloatArgument(BasicTypeArgument):
    TAG = GITypeTag.FLOAT
    py_type = float


class DoubleArgument(BasicTypeArgument):
    TAG = GITypeTag.DOUBLE
    py_type = float


class GTypeArgument(BasicTypeArgument):
    TAG = GITypeTag.GTYPE
    py_type = PGType


class VoidArgument(GIArgument):
    TAG = GITypeTag.VOID

    def setup(self):
        if self.type.is_pointer:
            self.py_type = int

    def pre_call(self):
        var = self.get_type()
        self.call_var = var.pack(var.check(self.name))
        return var.block


class GListArgument(GIArgument):
    TAG = GITypeTag.GLIST
    py_type = list


class Utf8Argument(GIArgument):
    TAG = GITypeTag.UTF8
    py_type = str

    def pre_call(self):
        var = self.get_type()

        if self.is_direction_inout():
            data = var.pack(var.check(self.name))

            if self.transfer_everything():
                data = var.dup(data)

            self.call_var = var.get_reference(data)
            self._data = data
        elif self.is_direction_in():
            self.call_var = var.pack(var.check(self.name))
        else:
            self._data = var.new()
            self.call_var = var.get_reference(self._data)

        return var.block

    def post_call(self):
        if not self.is_direction_out():
            return

        var = self.get_type()
        self.out_var = var.unpack(self._data)
        if self.transfer_everything():
            var.free(self._data)
        return var.block


class FilenameArgument(Utf8Argument):
    TAG = GITypeTag.FILENAME


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
