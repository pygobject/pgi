# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.gir import GITypeTag, GIInfoType, GITransfer, GIArrayType
from pgi.util import import_attribute
from pgi.gtype import PGType


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

    def setup(self):
        pass

    def pre_call(self):
        pass

    def post_call(self, name):
        return None, None

    def is_zero_terminated(self):
        return self.type.is_zero_terminated

    def is_pointer(self):
        return self.type.is_pointer

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
        return self.backend.unpack_bool(name)


class VoidReturnValue(ReturnValue):
    TAG = GITypeTag.VOID

    def setup(self):
        if self.is_pointer():
            self.py_type = int
        else:
            self.py_type = None

    def post_call(self, name):
        if self.is_pointer():
            return None, name
        else:
            return None, None


class ArrayReturnValue(ReturnValue):
    TAG = GITypeTag.ARRAY

    py_type = list

    def setup(self):
        self.array_length = self.type.array_length

        # mark other arg as aux so we handle it alone
        if self.array_length != -1:
            aux = self.args[self.array_length]
            aux.is_aux = True
            self._aux = aux

    def pre_call(self):
        if self.array_length != -1:
            block, var = self.backend.setup_int32()
            self._length_var = var

            block2, ref = self.backend.get_reference(var)
            block2.write_into(block)
            self._aux.call_var = ref
            return block

    def post_call(self, name):
        backend = self.backend
        array_type = self.type.array_type.value
        param_type = self.type.get_param_type(0)

        if array_type == GIArrayType.C:
            param_cls = get_return_class(param_type)
            param = param_cls(self.info, param_type, [], self.backend)

            if self.is_zero_terminated():
                block, var = backend.unpack_carray_zeroterm(name)
                return block, var
            else:
                # cast the gpointer to a pointer to the array type
                block, var = self.backend.cast_pointer(name, param_type)

                if self.type.array_length == -1:
                    # array size const
                    array_size = str(self.type.array_fixed_size)
                    # unpack array
                    block2, var = backend.unpack_carray_basic_fixed(var, array_size)
                    block2.write_into(block)
                else:
                    # filled by the aux
                    array_size = self._length_var
                    # unpack array
                    block2, var = backend.unpack_carray_basic_length(var, array_size)
                    block2.write_into(block)

                return block, var

        raise NotImplementedError("array return")


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
        block, var, ref = self.backend.unpack_utf8_return(name)
        if self.transfer_everything():
            block2 = self.backend.free_pointer(ref)
            block2.write_into(block)
        return block, var


class FilenameReturnValue(Utf8ReturnValue):
    TAG = GITypeTag.FILENAME
    py_type = str

    def post_call(self, name):
        return self.backend.unpack_utf8_return(name)[:2]


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
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        attr = import_attribute(iface_namespace, iface_name)
        return self.backend.unpack_enum(name, attr)


class InterfaceReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        block, out = self.backend.unpack_object(name)
        if self.transfer_nothing():
            block2 = self.backend.ref_object_null(out)
            block2.write_into(block)
        return block, out


class ObjectReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        block, out = self.backend.unpack_object(name)
        if self.transfer_nothing():
            block2 = self.backend.ref_object_null(out)
            block2.write_into(block)
        return block, out


class StructReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        attr = import_attribute(iface_namespace, iface_name)
        # we need to unpack GValues to match pygobject
        if iface_namespace == "GObject" and iface_name == "Value":
            #raise NotImplementedError
            block, out = self.backend.unpack_struct(name, attr)
            block2, out = self.backend.unpack_gvalue(out)
            block2.write_into(block)
            return block, out
        else:
            return self.backend.unpack_struct(name, attr)


class UnionReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        attr = import_attribute(iface_namespace, iface_name)
        return self.backend.unpack_union(name, attr)


class FlagsReturn(BaseInterfaceReturn):

    def post_call(self, name):
        iface = self.type.get_interface()
        iface_namespace = iface.namespace
        iface_name = iface.name

        attr = import_attribute(iface_namespace, iface_name)
        return self.backend.unpack_flags(name, attr)


class GTypeReturnValue(ReturnValue):
    TAG = GITypeTag.GTYPE
    py_type = PGType

    def post_call(self, name):
        return self.backend.unpack_gtype(name)


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
