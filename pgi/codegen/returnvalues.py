# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib.gir import GITypeTag, GIInfoType, GITransfer, GIArrayType
from pgi.gtype import PGType
from pgi.gerror import PGError


class ReturnValue(object):
    TAG = None

    py_type = None

    def __init__(self, info, type_, args, backend):
        super(ReturnValue, self).__init__()
        self.info = info
        self.type = type_
        self.backend = backend
        self.args = args

    @classmethod
    def get_class(cls, type_):
        return cls

    def get_type(self):
        return self.backend.get_type(self.type, self.info.may_return_null)

    def setup(self):
        pass

    def pre_call(self):
        pass

    def post_call(self, name):
        return None, None

    def is_zero_terminated(self):
        return self.type.is_zero_terminated

    def transfer_nothing(self):
        return self.info.caller_owns.value == GITransfer.NOTHING

    def transfer_container(self):
        return self.info.caller_owns.value == GITransfer.CONTAINER

    def transfer_everything(self):
        return self.info.caller_owns.value == GITransfer.EVERYTHING


class BooleanReturnValue(ReturnValue):
    TAG = GITypeTag.BOOLEAN

    py_type = bool

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


class VoidReturnValue(ReturnValue):
    TAG = GITypeTag.VOID

    def setup(self):
        if self.type.is_pointer:
            self.py_type = int
        else:
            self.py_type = None

    def post_call(self, name):
        # FIXME
        if self.type.is_pointer:
            return None, name
        else:
            return None, None


class ArrayReturn(ReturnValue):
    TAG = GITypeTag.ARRAY
    py_type = list

    @classmethod
    def get_class(cls, type_):
        value = type_.array_type.value

        if value == GIArrayType.C:
            return CArrayReturn

        raise NotImplementedError("Unsupported array return type")


class CArrayReturn(ArrayReturn):

    def setup(self):
        if self.type.array_length != -1:
            aux = self.args[self.type.array_length]
            aux.is_aux = True
            self._aux = aux

    def pre_call(self):
        if self.type.array_length != -1:
            var = self.backend.get_type(self._aux.type)
            self._length_var = var.new()
            self._aux.call_var = var.get_reference(self._length_var)
            return var.block

    def post_call(self, name):
        var = self.get_type()
        if self.type.array_length != -1:
            out = var.unpack(name, self._length_var)
        else:
            out = var.unpack(name, None)
        return var.block, out


class BasicReturnValue(ReturnValue):

    def post_call(self, name):
        return None, name


class UInt8ReturnValue(BasicReturnValue):
    TAG = GITypeTag.UINT8
    py_type = int


class Int8ReturnValue(BasicReturnValue):
    TAG = GITypeTag.INT8
    py_type = int


class Int16ReturnValue(BasicReturnValue):
    TAG = GITypeTag.INT16
    py_type = int


class UInt16ReturnValue(BasicReturnValue):
    TAG = GITypeTag.UINT16
    py_type = int


class Int32ReturnValue(BasicReturnValue):
    TAG = GITypeTag.INT32
    py_type = int


class UInt32ReturnValue(BasicReturnValue):
    TAG = GITypeTag.UINT32
    py_type = int


class Int64ReturnValue(BasicReturnValue):
    TAG = GITypeTag.INT64
    py_type = int


class UInt64ReturnValue(BasicReturnValue):
    TAG = GITypeTag.UINT64
    py_type = int


class DoubleReturnValue(BasicReturnValue):
    TAG = GITypeTag.DOUBLE
    py_type = float


class FloatReturnValue(BasicReturnValue):
    TAG = GITypeTag.FLOAT
    py_type = float


class Utf8ReturnValue(ReturnValue):
    TAG = GITypeTag.UTF8
    py_type = str

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack_return(name)
        if self.transfer_everything():
            var.free(name)
        return var.block, out


class ErrorReturn(ReturnValue):
    TAG = GITypeTag.ERROR
    py_type = PGError

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


class GListReturn(ReturnValue):
    TAG = GITypeTag.GLIST
    py_type = list


class FilenameReturnValue(Utf8ReturnValue):
    TAG = GITypeTag.FILENAME
    py_type = str


class BaseInterfaceReturn(ReturnValue):
    TAG = GITypeTag.INTERFACE
    py_type = object

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.ENUM:
            return EnumReturn
        elif iface_type == GIInfoType.OBJECT:
            return ObjectReturn
        elif iface_type == GIInfoType.INTERFACE:
            return InterfaceReturn
        elif iface_type == GIInfoType.STRUCT:
            return StructReturn
        elif iface_type == GIInfoType.UNION:
            return UnionReturn
        elif iface_type == GIInfoType.FLAGS:
            return FlagsReturn

        raise NotImplementedError(
            "Unsuported interface return type %r" % iface.type)


class EnumReturn(BaseInterfaceReturn):

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


class InterfaceReturn(BaseInterfaceReturn):

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        if self.transfer_nothing():
            var.ref(out)
        return var.block, out


class ObjectReturn(BaseInterfaceReturn):

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        if self.transfer_nothing():
            var.ref(out)
        return var.block, out


class StructReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        var = self.get_type()
        out = var.unpack(name)
        if iface_namespace == "GObject" and iface_name == "Value":
            out = var.unpack_gvalue(out)
        return var.block, out


class UnionReturn(BaseInterfaceReturn):

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


class FlagsReturn(BaseInterfaceReturn):

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


class GTypeReturnValue(ReturnValue):
    TAG = GITypeTag.GTYPE
    py_type = PGType

    def post_call(self, name):
        var = self.get_type()
        out = var.unpack(name)
        return var.block, out


_classes = {}


def _find_return_values():
    global _classes
    cls = [a for a in globals().values() if isinstance(a, type)]
    rv = ReturnValue
    retv = [a for a in cls if issubclass(a, rv) and a is not rv]
    _classes = dict(((a.TAG, a) for a in retv))
_find_return_values()


def get_return_class(type_):
    global _classes
    tag_value = type_.tag.value
    try:
        cls = _classes[tag_value]
    except KeyError:
        raise NotImplementedError("%r return not implemented" % type_.tag)
    else:
        return cls.get_class(type_)
