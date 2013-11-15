# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from .backend import Backend, VariableFactory
from .utils import CodeBlock, parse_with_objects

from pgi.clib.ctypesutil import gicast, find_library
from pgi.clib.gir import GICallableInfoPtr, GIStructInfoPtr
from pgi.clib.gir import GIRepositoryPtr, GITypeTag, GIInfoType, GIArrayType
from pgi.clib.glib import *
from pgi.clib.gobject import GCallback
from pgi.clib.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr, GType
from pgi.clib import glib
from pgi.gerror import PGError
from pgi.gtype import PGType
from pgi import foreign
from pgi.util import import_attribute


def typeinfo_to_ctypes(info, return_value=False):

    tag = info.tag.value
    ptr = info.is_pointer

    mapping = {
        GITypeTag.BOOLEAN: gboolean,
        GITypeTag.INT8: gint8,
        GITypeTag.UINT8: guint8,
        GITypeTag.INT16: gint16,
        GITypeTag.UINT16: guint16,
        GITypeTag.INT32: gint32,
        GITypeTag.UINT32: guint32,
        GITypeTag.INT64: gint64,
        GITypeTag.UINT64: guint64,
        GITypeTag.FLOAT: gfloat,
        GITypeTag.DOUBLE: gdouble,
        GITypeTag.VOID: None,
        GITypeTag.GTYPE: GType,
    }

    if ptr:
        if tag == GITypeTag.INTERFACE:
            return gpointer
        elif tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            if return_value:
                # ctypes does auto conversion to str and gives us no chance
                # to free the pointer if transfer=everything
                return gpointer
            else:
                return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
        elif tag == GITypeTag.ERROR:
            return GErrorPtr
        else:
            if tag in mapping:
                return ctypes.POINTER(mapping[tag])
    else:
        if tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            if iface_type == GIInfoType.ENUM:
                return guint32
            elif iface_type == GIInfoType.OBJECT:
                return gpointer
            elif iface_type == GIInfoType.STRUCT:
                return gpointer
            elif iface_type == GIInfoType.UNION:
                return gpointer
            elif iface_type == GIInfoType.FLAGS:
                return guint
            elif iface_type == GIInfoType.CALLBACK:
                return GCallback

            raise NotImplementedError(
                "Could not convert interface: %r to ctypes type" % iface.type)
        else:
            if tag in mapping:
                return mapping[tag]

    raise NotImplementedError("Could not convert %r to ctypes type" % info.tag)


def fixup_ctypes_kwargs(kwargs):
    # make ctypes dependencies local
    new_kwargs = {}
    for key, value in kwargs.iteritems():
        if isinstance(value, type) and value.__module__ == "ctypes":
            new_kwargs[key] = "%s.%s" % (value.__module__, value.__name__)
        else:
            new_kwargs[key] = value
    return new_kwargs


class BaseType(object):
    GI_TYPE_TAG = None
    py_type = None

    def __init__(self, gen, type_, may_be_null, may_return_null):
        self._gen = gen
        self.block = CodeBlock()
        self.type = type_
        self.may_be_null = may_be_null
        self.return_null = may_return_null

    def get_type(self, type_, may_be_null=False, may_return_null=False):
        return get_type(type_, self._gen, may_be_null, may_return_null)

    def var(self):
        return self._gen.var()

    @classmethod
    def get_class(cls, type_):
        return cls

    def parse(self, code, **kwargs):
        block, var = self._gen.parse(code, **fixup_ctypes_kwargs(kwargs))
        block.write_into(self.block)
        return var

    def get_reference(self, value):
        return self.parse("""
$ptr = ctypes.byref($value)
""", value=value)["ptr"]

    def free(self, name):
        self.parse("""
glib.free($ptr)
""", ptr=name)

        self.block.add_dependency("glib", glib)


class BasicType(BaseType):

    @classmethod
    def get_class(cls, type_):
        # no pointers for now
        if type_.is_pointer:
            raise NotImplementedError("basic type pointer")
        return cls

    def pack_in(self, name):
        return name

    def pre_unpack(self, c_value):
        # ctypes does auto unpacking of return values
        # to keep the unpack methods for out arguments and return values
        # the same, do the unpacking explicitly in the out arg case
        return self.parse("""
# unpack basic ctypes value
$value = $ctypes_value.value
""", ctypes_value=c_value)["value"]

    def unpack(self, name):
        return name


class Int8(BasicType):
    GI_TYPE_TAG = GITypeTag.INT8

    def check(self, name):
        return self.parse("""
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

# overflow check for int8
if not -2**7 <= $int < 2**7:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = ctypes.c_int8($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int8
$value = ctypes.c_int8()
""")["value"]


class UInt8(BasicType):
    GI_TYPE_TAG = GITypeTag.UINT8

    def check(self, name):
        return self.parse("""
# uint8 type/value check
if isinstance($value, basestring):
    if isinstance($value, str):
        try:
            $value = ord($value)
        except TypeError:
            raise TypeError("'$uint' must be a single character")
    else:
        raise TypeError("Input must be a str character")

$uint = int($value)

# overflow check for uint8
if not 0 <= $uint < 2**8:
    raise OverflowError("Value %r not in range" % $uint)
""", value=name)["uint"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = ctypes.c_uint8($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new uint8
$value = ctypes.c_uint8()
""")["value"]


class Int16(BasicType):
    GI_TYPE_TAG = GITypeTag.INT16

    def check(self, name):
        return self.parse("""
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

# overflow check for int16
if not -2**15 <= $int < 2**15:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = ctypes.c_int16($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int16
$value = ctypes.c_int16()
""")["value"]


class UInt16(BasicType):
    GI_TYPE_TAG = GITypeTag.UINT16

    def check(self, name):
        return self.parse("""
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

# overflow check for uint16
if not 0 <= $int < 2**16:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = ctypes.c_uint16($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int16
$value = ctypes.c_uint16()
""")["value"]


class Int32(BasicType):
    GI_TYPE_TAG = GITypeTag.INT32

    def check(self, name):
        return self.parse("""
# int32 type/value check
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

if not -2**31 <= $int < 2**31:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = ctypes.c_int32($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new int32
$value = ctypes.c_int32()
""")["value"]


class UInt32(BasicType):
    GI_TYPE_TAG = GITypeTag.UINT32

    def check(self, name):
        return self.parse("""
# uint32 type/value check
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

if not 0 <= $int < 2**32:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = ctypes.c_uint32($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new uint32
$value = ctypes.c_uint32()
""")["value"]


class Int64(BasicType):
    GI_TYPE_TAG = GITypeTag.INT64

    def check(self, name):
        return self.parse("""
# int64 type/value check
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

if not -2**63 <= $int < 2**63:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = ctypes.c_int64($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new int64
$value = ctypes.c_int64()
""")["value"]


class UInt64(BasicType):
    GI_TYPE_TAG = GITypeTag.UINT64

    def check(self, name):
        return self.parse("""
# uint64 type/value check
if not isinstance($value, basestring):
    $int = int($value)
else:
    raise TypeError("'$value' not a number")

if not 0 <= $int < 2**64:
    raise OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = ctypes.c_uint64($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new uint64
$value = ctypes.c_uint64()
""")["value"]


class Float(BasicType):
    GI_TYPE_TAG = GITypeTag.FLOAT

    def check(self, name):
        return self.parse("""
# float type/value check
if isinstance($value, basestring):
    raise TypeError
$float = float($value)
$c_float = ctypes.c_float($float)
$c_value = $c_float.value
if $c_value != $float and \\
        $c_value in (float('inf'), float('-inf'), float('nan')):
    raise OverflowError("%r out of range" % $float)
""", value=name)["c_float"]

    def pack(self, name):
        return name

    def new(self):
        return self.parse("""
# new float
$value = ctypes.c_float()
""")["value"]


class Double(BasicType):
    GI_TYPE_TAG = GITypeTag.DOUBLE

    def check(self, name):
        return self.parse("""
# double type/value check
if isinstance($value, basestring):
    raise TypeError
$double = float($value)
$c_double = ctypes.c_double($double)
$c_value = $c_double.value
if $c_value != $double and \\
        $c_value in (float('inf'), float('-inf'), float('nan')):
    raise OverflowError("%f out of range" % $double)
""", value=name)["c_double"]

    def pack(self, name):
        return name

    def new(self):
        return self.parse("""
# new double
$value = ctypes.c_double()
""")["value"]


class Boolean(BasicType):
    GI_TYPE_TAG = GITypeTag.BOOLEAN

    def check(self, name):
        return self.parse("""
$bool = bool($value)
""", value=name)["bool"]

    def pack(self, name):
        return self.parse("""
$c_bool = ctypes.c_int($value)
""", value=name)["c_bool"]

    def pre_unpack(self, name):
        return name

    def unpack(self, name):
        return self.parse("""
# pypy returns int instead of bool
$bool = bool($value)
""", value=name)["bool"]

    def new(self):
        return self.parse("""
$value = ctypes.c_int()
""")["value"]


class GType_(BaseType):
    GI_TYPE_TAG = GITypeTag.GTYPE

    def check(self, name):
        gtype_map = {
            str: "gchararray",
            int: "gint",
            float: "gdouble",
            bool: "gboolean",
        }

        items = gtype_map.items()
        gtype_map = dict((k, PGType.from_name(v)) for (k, v) in items)

        var = self.parse("""
if not isinstance($obj, PGType):
    if hasattr($obj, "__gtype__"):
        $obj = $obj.__gtype__
    elif $obj in $gtype_map:
        $obj = $gtype_map[$obj]

if not isinstance($obj, PGType):
    raise TypeError("%r not a GType" % $obj)
""", gtype_map=gtype_map, obj=name)

        self.block.add_dependency("PGType", PGType)

        return var["obj"]

    def pack(self, name):
        var = self.parse("""
$gtype = GType($obj._type.value)
""", obj=name)

        self.block.add_dependency("GType", GType)
        return var["gtype"]

    pack_in = pack

    def pre_unpack(self, name):
        return name

    def unpack(self, name):
        var = self.parse("""
$pgtype = PGType($gtype)
""", gtype=name)

        self.block.add_dependency("PGType", PGType)
        return var["pgtype"]

    def new(self):
        var = self.parse("""
$gtype = GType()
""")
        self.block.add_dependency("GType", GType)
        return var["gtype"]


class BaseInterface(BaseType):
    GI_TYPE_TAG = GITypeTag.INTERFACE

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.OBJECT:
            return Object
        elif iface_type == GIInfoType.INTERFACE:
            return Interface
        elif iface_type == GIInfoType.ENUM:
            return Enum
        elif iface_type == GIInfoType.FLAGS:
            return Flags
        elif iface_type == GIInfoType.STRUCT:
            return Struct
        elif iface_type == GIInfoType.CALLBACK:
            return Callback
        elif iface_type == GIInfoType.UNION:
            return Union

        raise NotImplementedError("Iface not implemented: %r" % iface.type)

    def _import_type(self):
        iface = self.type.get_interface()
        return import_attribute(iface.namespace, iface.name)


class Object(BaseInterface):

    def check(self, name):
        if self.may_be_null:
            return self.parse("""
if $obj is not None and not isinstance($obj, $type_class):
    raise TypeError("argument $obj: Expected %s, got %s" %
                    ($type_class.__name__, $obj.__class__.__name__))
""", obj=name, type_class=self._import_type())["obj"]

        return self.parse("""
if not isinstance($obj, $type_class):
    raise TypeError("argument $obj: Expected %s, got %s" %
                    ($type_class.__name__, $obj.__class__.__name__))
""", obj=name, type_class=self._import_type())["obj"]

    def pack(self, name):
        if self.may_be_null:
            return self.parse("""
$ptr = ctypes.c_void_p($obj and $obj._obj)
""", obj=name)["ptr"]

        return self.parse("""
$ptr = ctypes.c_void_p($obj._obj)
""", obj=name)["ptr"]

    def unpack(self, name):
        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = PGType(G_TYPE_FROM_INSTANCE(instance.contents))
            pytype = gtype.pytype
            if not pytype:
                raise RuntimeError("Couldn't find python type for %r" % gtype)
            return pytype

        return self.parse("""
# unpack object
if $value:
    $pyclass = $get_class($value)
    $obj = object.__new__($pyclass)
    $obj._obj = $value
else:
    $obj = None
""", value=name, get_class=get_class_func)["obj"]

    def ref(self, name):
            self.parse("""
if $obj:
    $obj._ref()
""", obj=name)

    def new(self):
        return self.parse("""
# new object
$value = ctypes.c_void_p()
""")["value"]


class Interface(Object):
    pass


class Union(BaseInterface):

    def unpack(self, name):
        return self.parse("""
# unpack union
$union = object.__new__($union_class)
$union._obj = $value
""", union_class=self._import_type(), value=name)["union"]


class Void(BaseType):
    GI_TYPE_TAG = GITypeTag.VOID

    def check(self, name):
        if self.may_be_null:
            return name

        return self.parse("""
if $ptr is None:
    raise TypeError("No None allowed")
""", ptr=name)["ptr"]

    def pack(self, name):
        assert self.type.is_pointer

        return self.parse("""
$c_ptr = ctypes.c_void_p($ptr)
""", ptr=name)["c_ptr"]

    def unpack(self, name):
        if self.type.is_pointer:
            return ""

        return self.parse("""
$value = $ptr.value
""", ptr=name)["value"]

    def new(self):
        assert self.type.is_pointer

        return self.parse("""
$c_ptr = ctypes.c_void_p()
""")["c_ptr"]


class Error(BaseType):
    GI_TYPE_TAG = GITypeTag.ERROR

    def unpack(self, name):
        var = self.parse("""
if $gerror_ptr:
    $out = PGError($gerror_ptr.contents)
else:
    $out = None
""", gerror_ptr=name)

        self.block.add_dependency("PGError", PGError)
        return var["out"]

    def check_raise(self, name):
        self.parse("""
if $error:
    raise $error
""", error=name)

    def new(self):
        return self.parse("""
$ptr = $gerror_ptr()
""", gerror_ptr=GErrorPtr)["ptr"]

    def free(self, name):
        self.parse("""
if $ptr:
    $ptr.free()
""", ptr=name)


class Utf8(BaseType):
    GI_TYPE_TAG = GITypeTag.UTF8

    def check(self, name):
        if self.may_be_null:
            return self.parse("""
if $value is not None:
    if isinstance($value, unicode):
        $string = $value.encode("utf-8")
    elif not isinstance($value, str):
        raise TypeError("%r not a string or None" % $value)
    else:
        $string = $value
else:
    $string = None
""", value=name)["string"]

        return self.parse("""
if isinstance($value, unicode):
    $string = $value.encode("utf-8")
elif not isinstance($value, str):
    raise TypeError("%r not a string" % $value)
else:
    $string = $value
""", value=name)["string"]

    def pack(self, name):
        return self.parse("""
$c_value = ctypes.c_char_p($value)
""", value=name)["c_value"]

    def dup(self, name):
        var = self.parse("""
if $ptr:
    $ptr_cpy = ctypes.c_char_p(glib.g_strdup($ptr))
else:
    $ptr_cpy = None
""", ptr=name)

        self.block.add_dependency("glib", glib)
        return var["ptr_cpy"]

    def unpack(self, name):
        return self.parse("""
$value = $ctypes_value.value
""", ctypes_value=name)["value"]

    def unpack_return(self, name):
        return self.parse("""
$str_value = ctypes.c_char_p($value).value
""", value=name)["str_value"]

    def new(self):
        return self.parse("""
$value = ctypes.c_char_p()
""")["value"]


class Filename(Utf8):
    GI_TYPE_TAG = GITypeTag.FILENAME


class Enum(BaseInterface):

    def check(self, name):
        return self.parse("""
if $value not in $base_type._allowed:
    raise TypeError("Invalid enum: %r" % $value)
""", base_type=self._import_type(), value=name)["value"]

    def pack(self, name):
        return self.parse("""
$c_value = ctypes.c_uint($value)
""", value=name)["c_value"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        return self.parse("""
$enum = $enum_class($value)
""", enum_class=self._import_type(), value=name)["enum"]

    def new(self):
        return self.parse("""
$val = ctypes.c_uint()
""")["val"]


class Flags(BaseInterface):

    def check(self, name):
        return self.parse("""
if not isinstance($value, basestring) and not int($value):
    $out = 0
elif isinstance($value, $base_type):
    $out = int($value)
else:
    raise TypeError("Expected %r but got %r" %
                    ($base_type.__name__, type($value).__name__))
""", base_type=self._import_type(), value=name)["out"]

    def pack(self, name):
        return self.parse("""
$c_value = ctypes.c_uint($value)
""", value=name)["c_value"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        return self.parse("""
$flags = $flags_class($value)
""", flags_class=self._import_type(), value=name)["flags"]

    def new(self):
        return self.parse("""
$val = ctypes.c_uint()
""")["val"]


class Struct(BaseInterface):

    def check(self, name):
        base_obj = import_attribute("GObject", "Object")

        return self.parse("""
if not isinstance($obj, ($struct_class, $obj_class)):
    raise TypeError("%r is not a structure object" % $obj)
""", obj_class=base_obj, struct_class=self._import_type(), obj=name)["obj"]

    def pack(self, name):
        return self.parse("""
$out = ctypes.c_void_p($obj._obj)
""", obj=name)["out"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        iface = gicast(self.type.get_interface(), GIStructInfoPtr)
        foreign_struct = None
        if iface.is_foreign:
            foreign_struct = foreign.get_foreign(iface.namespace, iface.name)

        if foreign_struct:
            return self.parse("""
if $obj:
    $new_foreign = $foreign.from_pointer($obj)
else:
    $new_foreign = $obj
""", obj=name, foreign=foreign_struct)["new_foreign"]

        return self.parse("""
if $value:
    $obj = object.__new__($type)
    $obj._obj = $value
else:
    $obj = None
""", value=name, type=self._import_type())["obj"]

    def new(self):
        return self.parse("""
$value = ctypes.c_void_p()
""")["value"]

    def alloc(self):
        struct_class = self._import_type()
        size = struct_class._size
        malloc = glib.g_try_malloc0

        return self.parse("""
$mem = $malloc($size)
if not $mem and $size:
    raise MemoryError
$value = ctypes.c_void_p($mem)
""", malloc=malloc, size=size)["value"]

    def unpack_gvalue(self, name):
        getter_map = {
            "gboolean": lambda v: v.get_boolean(),
            "gchar": lambda v: chr(v.get_schar()),
            "gdouble": lambda v: v.get_double(),
            "gfloat": lambda v: v.get_float(),
            "GType": lambda v: v.get_gtype(),
            "gint64": lambda v: v.get_int64(),
            "gint": lambda v: v.get_int(),
            "glong": lambda v: v.get_long(),
            "GObject": lambda v: v.get_object(),
            "gpointer": lambda v: v.get_pointer(),
            "gchararray": lambda v: v.get_string(),
            "guchar": lambda v: chr(v.get_uchar()),
            "guint64": lambda v: v.get_uint64(),
            "guint": lambda v: v.get_uint(),
            "gulong": lambda v: v.get_ulong(),
        }

        items = getter_map.items()
        getter_map = dict((PGType.from_name(k), v) for (k, v) in items)

        return self.parse("""
try:
    $out = $lookup[$value.g_type]($value)
except KeyError:
    $out = $value
""", value=name, lookup=getter_map)["out"]


class Callback(BaseInterface):

    def check(self, name):
        return self.parse("""
if not callable($py_cb):
    raise TypeError("%r must be callable" % $py_cb)
""", py_cb=name)["py_cb"]

    def pack(self, name):
        from pgi.codegen.siggen import generate_callback
        interface = gicast(self.type.get_interface(), GICallableInfoPtr)
        pack_func, docstring = generate_callback(interface)

        return self.parse("""
$ctypes_cb = $pack_func($py_cb)
""", pack_func=pack_func, py_cb=name)["ctypes_cb"]


class BaseArray(BaseType):
    GI_TYPE_TAG = GITypeTag.ARRAY

    @classmethod
    def get_class(cls, type_):
        type_ = type_.array_type.value

        if type_ == GIArrayType.C:
            return CArray

        raise NotImplementedError("unsupported array type: %r" % type_)


class CArray(BaseArray):

    def check(self, name):
        if self.type.array_fixed_size != -1:
            length = str(self.type.array_fixed_size)
            self.parse("""
if len($l) != $length:
    raise ValueError("Expected list of length %d, got $length" % len($l))
""", l=name, length=length)
        return name

    def pack(self, name, length_type):
        # length
        if self.type.array_length != -1:
            l = self.get_type(length_type)
            length = l.parse("$len = len($inp)", inp=name)["len"]
            packed_length = l.pack(length)
            l.block.write_into(self.block)
        elif self.type.array_fixed_size != -1:
            length = str(self.type.array_fixed_size)
            packed_length = ""
        else:
            length = self.parse("$len = len($inp)", inp=name)["len"]
            packed_length = ""

        # param
        param_type = self.type.get_param_type(0)
        p = self.get_type(param_type)
        item_in = self.var()
        item_out = p.pack(p.check(item_in))
        ctypes_type = typeinfo_to_ctypes(param_type)

        # array zero term
        if self.type.is_zero_terminated:
            return self.parse("""
$array = ($ctypes_type * ($length + 1))()
for $i, $item_in in enumerate($name):
    $param_pack
    $array[$i] = $item_out
$array[-1] = $ctypes_type()
$array_ptr = ctypes.pointer($array)
    """, name=name, item_in=item_in, item_out=item_out, param_pack=p.block,
         ctypes_type=ctypes_type, length=length)["array_ptr"], packed_length

        # non zero term
        return self.parse("""
$array = ($ctypes_type * $length)()
for $i, $item_in in enumerate($name):
    $param_pack
    $array[$i] = $item_out
$array_ptr = ctypes.pointer($array)
""", name=name, item_in=item_in, item_out=item_out, param_pack=p.block,
     ctypes_type=ctypes_type, length=length)["array_ptr"], packed_length

    def unpack(self, name, length):
        param_type = self.type.get_param_type(0)
        ctypes_type = typeinfo_to_ctypes(param_type)

        data = self.parse("""
$data = ctypes.cast($value, ctypes.POINTER($type))
""", value=name, type=ctypes_type)["data"]

        # fixme: do unpack with param type

        if self.type.array_length != -1:
            return self.parse("""
$out = $array[:$length.value]
""", array=data, length=length)["out"]
        elif self.type.array_fixed_size != -1:
            return self.parse("""
$out = $array[:$length]
""", array=data, length=str(self.type.array_fixed_size))["out"]
        else:
            return self.parse("""
$list = []
$i = 0
$current = $array and $array[$i]
while $current:
    $list.append($current)
    $i += 1
    $current = $array[$i]
""", array=data)["list"]

    def new(self, length_type):
        if self.type.array_length != -1:
            l = self.get_type(length_type)
            packed_length = l.new()
            l.block.write_into(self.block)
        else:
            packed_length = ""

        if self.type.is_zero_terminated or self.type.array_length != -1:
            return self.parse("""
$array = ctypes.c_void_p()
""")["array"], packed_length
        elif self.type.array_fixed_size != -1:
            param_type = self.type.get_param_type(0)
            ctypes_type = typeinfo_to_ctypes(param_type)
            length = str(self.type.array_fixed_size)

            return self.parse("""
$data = ($ctypes_type * $length)()
$array = ctypes.pointer($data)
""", ctypes_type=ctypes_type, length=length)["array"], packed_length
        else:
            raise NotImplementedError


class CTypesCodeGen(object):
    def __init__(self, var):
        self.var = var

    def parse(self, code, **kwargs):
        block, var = parse_with_objects(code, self.var, **kwargs)
        block.add_dependency("ctypes", ctypes)
        return block, var


def get_type(type_, gen, may_be_null, may_return_null):
    tag_value = type_.tag.value
    for obj in globals().values():
        if isinstance(obj, type) and issubclass(obj, BaseType):
            if obj.GI_TYPE_TAG == tag_value:
                cls = obj
                break
    else:
        raise NotImplementedError("type: %r", type_.tag)

    cls = cls.get_class(type_, )
    return cls(gen, type_, may_be_null, may_return_null)


class CTypesBackend(Backend):
    NAME = "ctypes"
    _libs = {}

    def __init__(self):
        Backend.__init__(self)
        self._gen = CTypesCodeGen(VariableFactory())

    def var(self):
        return self._gen.var()

    def get_type(self, type_, may_be_null=False, may_return_null=False):
        return get_type(type_, self._gen, may_be_null, may_return_null)

    def get_library(self, namespace):
        if namespace not in self._libs:
            paths = GIRepositoryPtr().get_shared_library(namespace)
            if not paths:
                return
            path = paths.split(",")[0]
            lib = ctypes.cdll.LoadLibrary(path)
            self._libs[namespace] = lib
        return self._libs[namespace]

    def get_function(self, lib, symbol, args, ret,
                     method=False, self_name="", throws=False):
        try:
            h = getattr(lib, symbol)
        except AttributeError:
            raise NotImplementedError(
                "Library doesn't provide symbol: %s" % symbol)

        if ret:
            h.restype = typeinfo_to_ctypes(ret.type, return_value=True)
        else:
            h.restype = None

        arg_types = []

        if method:
            arg_types.append(ctypes.c_void_p)

        if throws:
            args = args[:-1]

        for arg in args:
            type_ = typeinfo_to_ctypes(arg.type)
            if arg.is_direction_out() and type_ != ctypes.c_void_p:
                type_ = ctypes.POINTER(type_)
            arg_types.append(type_)

        if throws:
            arg_types.append(ctypes.c_void_p)

        h.argtypes = arg_types

        block, var = self.parse("""
# args: $args
# ret: $ret
""", args=repr([n.__name__ for n in h.argtypes]), ret=repr(h.restype))

        return block, method and "%s._obj" % self_name, h

    def get_callback(self, func, args, ret, is_signal=False):
        arg_types = [typeinfo_to_ctypes(a.type) for a in args]
        # skip the first arg, we pass the signal's object manually
        if is_signal:
            arg_types.insert(0, ctypes.c_void_p)
        ret_type = typeinfo_to_ctypes(ret.type)
        cb_object_type = ctypes.CFUNCTYPE(ret_type, *arg_types)
        return ctypes.cast(cb_object_type(func), GCallback)

    def get_constructor(self, gtype, args):
        # we need to create a new library, or the argtypes change for all
        # instances
        lib = find_library("gobject-2.0", cached=False)
        h = getattr(lib, "g_object_new")

        arg_types = [GType]
        for arg in args:
            arg_types.append(ctypes.c_char_p)
            arg_types.append(typeinfo_to_ctypes(arg.type))
        arg_types.append(ctypes.c_void_p)
        h.argtypes = arg_types
        h.restype = ctypes.c_void_p

        values = []
        for arg in args:
            values.append("'%s'" % arg.name)
            values.append(arg.out_var)
        values.append("None")
        type_ = gtype._type

        block, var = self.parse("""
# args: $args
# ret: $ret
$out = $func($type_num, $values)
""", args=repr([n.__name__ for n in h.argtypes]), ret=repr(h.restype),
        type_num=type_, values=", ".join(values), func=h)

        return block, var["out"]

    def parse(self, code, **kwargs):
        return self._gen.parse(code, **fixup_ctypes_kwargs(kwargs))

    def cast_pointer(self, name, type_):
        block, var = self.parse("""
$value = ctypes.cast($value, ctypes.POINTER($type))
""", value=name, type=typeinfo_to_ctypes(type_))

        return block, name

    def deref_pointer(self, name):
        block, var = self.parse("""
$value = $value.contents
""", value=name)

        return block, var["value"]

    def assign_pointer(self, ptr, value):
        block, var = self.parse("""
$ptr[0] = $value
""", ptr=ptr, value=value)

        return block
