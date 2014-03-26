# Copyright 2012-2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib import glib
from pgi.clib.gir import GITypeTag
from pgi import _compat

from .utils import BaseType, register_type


class BasicType(BaseType):

    @classmethod
    def get_class(cls, type_):
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


@register_type(GITypeTag.BOOLEAN)
class Boolean(BasicType):

    def check(self, name):
        return self.parse("""
$bool = $_.bool($value)
""", value=name)["bool"]

    def pack(self, name):
        return self.parse("""
$c_bool = $ctypes.c_int($value)
""", value=name)["c_bool"]

    def pre_unpack(self, name):
        return name

    def unpack(self, name):
        return self.parse("""
# pypy returns int instead of bool
$bool = $_.bool($value)
""", value=name)["bool"]

    def new(self):
        return self.parse("""
$value = $ctypes.c_int()
""")["value"]


@register_type(GITypeTag.INT8)
class Int8(BasicType):

    def check(self, name):
        return self.parse("""
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise TypeError("'$value' not a number")

# overflow check for int8
if not -2**7 <= $int < 2**7:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = $ctypes.c_int8($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int8
$value = $ctypes.c_int8()
""")["value"]


@register_type(GITypeTag.UINT8)
class UInt8(BasicType):

    def check(self, name):

        if _compat.PY3:
            int_text_types = (str, bytes)
        else:
            int_text_types = (unicode, str)

        return self.parse("""
# uint8 type/value check
if $_.isinstance($value, $text_types):
    if $_.isinstance($value, $_.bytes):
        try:
            $value = $_.ord($value)
        except $_.TypeError:
            raise $_.TypeError("'$uint' must be a single character")
    else:
        raise $_.TypeError("Input must be a str character")

$uint = $_.int($value)

# overflow check for uint8
if not 0 <= $uint < 2**8:
    raise $_.OverflowError("Value %r not in range" % $uint)
""", value=name, text_types=int_text_types)["uint"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = $ctypes.c_uint8($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new uint8
$value = $ctypes.c_uint8()
""")["value"]


@register_type(GITypeTag.INT16)
class Int16(BasicType):

    def check(self, name):
        return self.parse("""
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

# overflow check for int16
if not -2**15 <= $int < 2**15:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = $ctypes.c_int16($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int16
$value = $ctypes.c_int16()
""")["value"]


@register_type(GITypeTag.UINT16)
class UInt16(BasicType):

    def check(self, name):
        return self.parse("""
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

# overflow check for uint16
if not 0 <= $int < 2**16:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, name):
        return self.parse("""
# to ctypes
$cvalue = $ctypes.c_uint16($value)
""", value=name)["cvalue"]

    def new(self):
        return self.parse("""
# new int16
$value = $ctypes.c_uint16()
""")["value"]


@register_type(GITypeTag.INT32)
class Int32(BasicType):

    def check(self, name):
        return self.parse("""
# int32 type/value check
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

if not -2**31 <= $int < 2**31:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = $ctypes.c_int32($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new int32
$value = $ctypes.c_int32()
""")["value"]

    def pack_pointer(self, name):
        return self.parse("""
$ptr = $in_
""", in_=name)["ptr"]


@register_type(GITypeTag.UINT32)
class UInt32(BasicType):

    def check(self, name):
        return self.parse("""
# uint32 type/value check
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

if not 0 <= $int < 2**32:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = $ctypes.c_uint32($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new uint32
$value = $ctypes.c_uint32()
""")["value"]

    def pack_pointer(self, name):
        return self.parse("""
$ptr = $in_
""", in_=name)["ptr"]


@register_type(GITypeTag.INT64)
class Int64(BasicType):

    def check(self, name):
        return self.parse("""
# int64 type/value check
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

if not -2**63 <= $int < 2**63:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = $ctypes.c_int64($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new int64
$value = $ctypes.c_int64()
""")["value"]


@register_type(GITypeTag.UINT64)
class UInt64(BasicType):

    def check(self, name):
        return self.parse("""
# uint64 type/value check
if not $_.isinstance($value, $basestring):
    $int = $_.int($value)
else:
    raise $_.TypeError("'$value' not a number")

if not 0 <= $int < 2**64:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name, basestring=_compat.string_types)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = $ctypes.c_uint64($value)
""", value=valid)["c_value"]

    def new(self):
        return self.parse("""
# new uint64
$value = $ctypes.c_uint64()
""")["value"]


@register_type(GITypeTag.FLOAT)
class Float(BasicType):

    def check(self, name):
        return self.parse("""
# float type/value check
if $_.isinstance($value, $basestring):
    raise $_.TypeError
$float = $_.float($value)
$c_float = $ctypes.c_float($float)
$c_value = $c_float.value
if $c_value != $float and \\
        $c_value in ($_.float('inf'), $_.float('-inf'), $_.float('nan')):
    raise $_.OverflowError("%r out of range" % $float)
""", value=name, basestring=_compat.string_types)["c_float"]

    def pack(self, name):
        return name

    def new(self):
        return self.parse("""
# new float
$value = $ctypes.c_float()
""")["value"]


@register_type(GITypeTag.DOUBLE)
class Double(BasicType):

    def check(self, name):
        return self.parse("""
# double type/value check
if $_.isinstance($value, $basestring):
    raise $_.TypeError
$double = $_.float($value)
$c_double = $ctypes.c_double($double)
$c_value = $c_double.value
if $c_value != $double and \\
        $c_value in ($_.float('inf'),$_.float('-inf'), $_.float('nan')):
    raise $_.OverflowError("%f out of range" % $double)
""", value=name, basestring=_compat.string_types)["c_double"]

    def pack(self, name):
        return name

    def new(self):
        return self.parse("""
# new double
$value = $ctypes.c_double()
""")["value"]


@register_type(GITypeTag.UNICHAR)
class UniChar(BasicType):

    def check_py2(self, name):
        return self.parse("""
if $_.isinstance($value, $_.str):
    $value = $value.decode("utf-8")
elif not isinstance($value, $_.unicode):
    raise $_.TypeError

$int = $_.ord($value)

if not 0 <= $int < 2**32:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def check_py3(self, name):
        return self.parse("""
$int = $_.ord($value)

if not 0 <= $int < 2**32:
    raise $_.OverflowError("Value %r not in range" % $int)
""", value=name)["int"]

    def pack(self, valid):
        return self.parse("""
# to ctypes
$c_value = $ctypes.c_uint32($value)
""", value=valid)["c_value"]

    def unpack_return_py2(self, name):
        return self.parse("""
$out = $_.unichr($value).encode("utf-8")
""", value=name)["out"]

    def unpack_return_py3(self, name):
        return self.parse("""
$out = $_.chr($value)
""", value=name)["out"]

    def new(self):
        return self.parse("""
# new uint32
$value = $ctypes.c_uint32()
""")["value"]

    def pack_pointer(self, name):
        return self.parse("""
$ptr = $in_
""", in_=name)["ptr"]


@register_type(GITypeTag.VOID)
class Void(BaseType):

    def check(self, name):
        if self.may_be_null:
            return name

        return self.parse("""
if $ptr is None:
    raise $_.TypeError("No None allowed")
""", ptr=name)["ptr"]

    def pack(self, name):
        assert self.type.is_pointer

        return self.parse("""
$c_ptr = $ctypes.c_void_p($ptr)
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
$c_ptr = $ctypes.c_void_p()
""")["c_ptr"]


@register_type(GITypeTag.UTF8)
class Utf8(BaseType):

    def check_py3(self, name):
        if self.may_be_null:
            return self.parse("""
if $value is not None:
    if not $_.isinstance($value, $_.str):
        raise $_.TypeError("%r not a string or None" % $value)
    else:
        $string = $value
else:
    $string = None
""", value=name)["string"]

        return self.parse("""
if not isinstance($value, $_.str):
    raise $_.TypeError("%r not a string" % $value)
else:
    $string = $value
""", value=name)["string"]

    def check_py2(self, name):
        if self.may_be_null:
            return self.parse("""
if $value is not None:
    if $_.isinstance($value, $_.unicode):
        $string = $value.encode("utf-8")
    elif not $_.isinstance($value, $_.str):
        raise $_.TypeError("%r not a string or None" % $value)
    else:
        $string = $value
else:
    $string = None
""", value=name)["string"]

        return self.parse("""
if $_.isinstance($value, $_.unicode):
    $string = $value.encode("utf-8")
elif not isinstance($value, $_.str):
    raise $_.TypeError("%r not a string" % $value)
else:
    $string = $value
""", value=name)["string"]

    def pack_in_py2(self, name):
        return name

    def pack_in_py3(self, name):
        return self.parse("""
$encoded = $value
if $value is not None:
    $encoded = $value.encode("utf-8")
""", value=name)["encoded"]

    def pack_py2(self, name):
        return self.parse("""
$c_value = $ctypes.c_char_p($value)
""", value=name)["c_value"]

    def pack_py3(self, name):
        return self.parse("""
if $value is not None:
    $value = $value.encode("utf-8")
$c_value = $ctypes.c_char_p($value)
""", value=name)["c_value"]

    def dup(self, name):
        var = self.parse("""
if $ptr:
    $ptr_cpy = $ctypes.c_char_p($glib.g_strdup($ptr))
else:
    $ptr_cpy = $none
""", ptr=name, glib=glib, none=None)

        return var["ptr_cpy"]

    def pre_unpack(self, c_value):
        return self.parse("""
$value = $ctypes_value.value
""", ctypes_value=c_value)["value"]

    def unpack_py2(self, name):
        return self.parse("""
$value = $ctypes_value
""", ctypes_value=name)["value"]

    def unpack_py3(self, name):
        return self.parse("""
if $value is not None:
    $value = $value.decode("utf-8")
""", value=name, none=None)["value"]

    def unpack_return_py2(self, name):
        return self.parse("""
$str_value = $ctypes.c_char_p($value).value
""", value=name)["str_value"]

    def unpack_return_py3(self, name):
        return self.parse("""
$str_value = $ctypes.c_char_p($value).value
if $str_value is not None:
    $str_value = $str_value.decode("utf-8")
""", value=name)["str_value"]

    def new(self):
        return self.parse("""
$value = $ctypes.c_char_p()
""")["value"]

    def pack_pointer(self, name):
        return self.parse("""
$ptr = ord($in_)
""", in_=name)["ptr"]


@register_type(GITypeTag.FILENAME)
class Filename(Utf8):
    pass
