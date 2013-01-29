# coding=utf-8
# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import tempfile
import shutil
import unittest
import os
import sys

from tests import is_gi
from pgi.gir import *
search_path = os.path.dirname(__file__)
GIRepository.prepend_search_path(search_path)

try:
    from gi.repository import GIMarshallingTests
except ImportError:
    GIMarshallingTests = None

import gi
from gi.repository import GObject, GLib

from compathelper import _bytes, _unicode

if sys.version_info < (3, 0):
    CONSTANT_UTF8 = "const \xe2\x99\xa5 utf8"
    PY2_UNICODE_UTF8 = unicode(CONSTANT_UTF8, 'UTF-8')
    CHAR_255 = '\xff'
else:
    CONSTANT_UTF8 = "const ♥ utf8"
    CHAR_255 = bytes([255])

CONSTANT_NUMBER = 42


class Number(object):

    def __init__(self, value):
        self.value = value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)


class Sequence(object):

    def __init__(self, sequence):
        self.sequence = sequence

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, key):
        return self.sequence[key]


class TestConstant(unittest.TestCase):

# Blocked by https://bugzilla.gnome.org/show_bug.cgi?id=595773
#    def test_constant_utf8(self):
#        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.CONSTANT_UTF8)

    @unittest.skipUnless(GIMarshallingTests, "")
    def test_constant_number(self):
        self.assertEqual(CONSTANT_NUMBER, GIMarshallingTests.CONSTANT_NUMBER)

    def test_min_max_int(self):
        self.assertEqual(GLib.MAXINT32, 2 ** 31 - 1)
        self.assertEqual(GLib.MININT32, -2 ** 31)
        self.assertEqual(GLib.MAXUINT32, 2 ** 32 - 1)

        self.assertEqual(GLib.MAXINT64, 2 ** 63 - 1)
        self.assertEqual(GLib.MININT64, -2 ** 63)
        self.assertEqual(GLib.MAXUINT64, 2 ** 64 - 1)


@unittest.skipUnless(GIMarshallingTests, "")
class TestBoolean(unittest.TestCase):

    def test_boolean_return(self):
        self.assertEqual(True, GIMarshallingTests.boolean_return_true())
        self.assertEqual(False, GIMarshallingTests.boolean_return_false())

    def test_boolean_in(self):
        GIMarshallingTests.boolean_in_true(True)
        GIMarshallingTests.boolean_in_false(False)

        GIMarshallingTests.boolean_in_true(1)
        GIMarshallingTests.boolean_in_false(0)

    def test_boolean_out(self):
        self.assertEqual(True, GIMarshallingTests.boolean_out_true())
        self.assertEqual(False, GIMarshallingTests.boolean_out_false())

    def test_boolean_inout(self):
        self.assertEqual(False, GIMarshallingTests.boolean_inout_true_false(True))
        self.assertEqual(True, GIMarshallingTests.boolean_inout_false_true(False))


@unittest.skipUnless(GIMarshallingTests, "")
class TestInt8(unittest.TestCase):

    MAX = GObject.G_MAXINT8
    MIN = GObject.G_MININT8

    def test_int8_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int8_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int8_return_min())

    def test_int8_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int8_in_max(max)
        GIMarshallingTests.int8_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int8_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int8_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int8_in_max, "self.MAX")

    def test_int8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int8_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int8_out_min())

    def test_int8_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int8_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int8_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestUInt8(unittest.TestCase):

    MAX = GObject.G_MAXUINT8

    def test_uint8_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_return())

    def test_uint8_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint8_in(number)
        GIMarshallingTests.uint8_in(CHAR_255)

        number.value += 1
        self.assertRaises(ValueError, GIMarshallingTests.uint8_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint8_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint8_in, "self.MAX")

    def test_uint8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_out())

    def test_uint8_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint8_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestInt16(unittest.TestCase):

    MAX = GObject.G_MAXINT16
    MIN = GObject.G_MININT16

    def test_int16_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int16_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int16_return_min())

    def test_int16_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int16_in_max(max)
        GIMarshallingTests.int16_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int16_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int16_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int16_in_max, "self.MAX")

    def test_int16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int16_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int16_out_min())

    def test_int16_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int16_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int16_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestUInt16(unittest.TestCase):

    MAX = GObject.G_MAXUINT16

    def test_uint16_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_return())

    def test_uint16_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint16_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint16_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint16_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint16_in, "self.MAX")

    def test_uint16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_out())

    def test_uint16_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint16_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestInt32(unittest.TestCase):

    MAX = GObject.G_MAXINT32
    MIN = GObject.G_MININT32

    def test_int32_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int32_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int32_return_min())

    def test_int32_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int32_in_max(max)
        GIMarshallingTests.int32_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int32_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int32_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int32_in_max, "self.MAX")

    def test_int32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int32_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int32_out_min())

    def test_int32_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int32_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int32_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestUInt32(unittest.TestCase):

    MAX = GObject.G_MAXUINT32

    def test_uint32_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_return())

    def test_uint32_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint32_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint32_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint32_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint32_in, "self.MAX")

    def test_uint32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_out())

    def test_uint32_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint32_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestInt64(unittest.TestCase):

    MAX = 2 ** 63 - 1
    MIN = - (2 ** 63)

    def test_int64_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int64_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int64_return_min())

    def test_int64_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int64_in_max(max)
        GIMarshallingTests.int64_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int64_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int64_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int64_in_max, "self.MAX")

    def test_int64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int64_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int64_out_min())

    def test_int64_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int64_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int64_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestUInt64(unittest.TestCase):

    MAX = 2 ** 64 - 1

    def test_uint64_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_return())

    def test_uint64_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint64_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint64_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint64_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint64_in, "self.MAX")

    def test_uint64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_out())

    def test_uint64_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint64_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestShort(unittest.TestCase):

    MAX = GObject.G_MAXSHORT
    MIN = GObject.G_MINSHORT

    def test_short_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.short_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.short_return_min())

    def test_short_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.short_in_max(max)
        GIMarshallingTests.short_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.short_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.short_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.short_in_max, "self.MAX")

    def test_short_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.short_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.short_out_min())

    def test_short_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.short_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.short_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestUShort(unittest.TestCase):

    MAX = GObject.G_MAXUSHORT

    def test_ushort_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_return())

    def test_ushort_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ushort_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.ushort_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.ushort_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ushort_in, "self.MAX")

    def test_ushort_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_out())

    def test_ushort_inout(self):
        self.assertEqual(0, GIMarshallingTests.ushort_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestInt(unittest.TestCase):

    MAX = GObject.G_MAXINT
    MIN = GObject.G_MININT

    def test_int_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int_return_min())

    def test_int_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int_in_max(max)
        GIMarshallingTests.int_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int_in_max, "self.MAX")

    def test_int_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int_out_min())

    def test_int_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int_inout_min_max(Number(self.MIN)))
        self.assertRaises(TypeError, GIMarshallingTests.int_inout_min_max, Number(self.MIN), CONSTANT_NUMBER)


@unittest.skipUnless(GIMarshallingTests, "")
class TestUInt(unittest.TestCase):

    MAX = GObject.G_MAXUINT

    def test_uint_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_return())

    def test_uint_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint_in, "self.MAX")

    def test_uint_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_out())

    def test_uint_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestLong(unittest.TestCase):

    MAX = GObject.G_MAXLONG
    MIN = GObject.G_MINLONG

    def test_long_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.long_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.long_return_min())

    def test_long_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.long_in_max(max)
        GIMarshallingTests.long_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.long_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.long_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.long_in_max, "self.MAX")

    def test_long_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.long_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.long_out_min())

    def test_long_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.long_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.long_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestULong(unittest.TestCase):

    MAX = GObject.G_MAXULONG

    def test_ulong_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_return())

    def test_ulong_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ulong_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.ulong_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.ulong_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ulong_in, "self.MAX")

    def test_ulong_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_out())

    def test_ulong_inout(self):
        self.assertEqual(0, GIMarshallingTests.ulong_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestSSize(unittest.TestCase):

    MAX = GObject.G_MAXLONG
    MIN = GObject.G_MINLONG

    def test_ssize_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_return_min())

    def test_ssize_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.ssize_in_max(max)
        GIMarshallingTests.ssize_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.ssize_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.ssize_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.ssize_in_max, "self.MAX")

    def test_ssize_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_out_min())

    def test_ssize_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_inout_min_max(Number(self.MIN)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestSize(unittest.TestCase):

    MAX = GObject.G_MAXULONG

    def test_size_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_return())

    def test_size_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.size_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.size_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.size_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.size_in, "self.MAX")

    def test_size_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_out())

    def test_size_inout(self):
        self.assertEqual(0, GIMarshallingTests.size_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestFloat(unittest.TestCase):

    MAX = GObject.G_MAXFLOAT
    MIN = GObject.G_MINFLOAT

    def test_float_return(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.float_return())

    def test_float_in(self):
        GIMarshallingTests.float_in(Number(self.MAX))

        self.assertRaises(TypeError, GIMarshallingTests.float_in, "self.MAX")

    def test_float_out(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.float_out())

    def test_float_inout(self):
       self.assertAlmostEqual(self.MIN, GIMarshallingTests.float_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestDouble(unittest.TestCase):

    MAX = GObject.G_MAXDOUBLE
    MIN = GObject.G_MINDOUBLE

    def test_double_return(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.double_return())

    def test_double_in(self):
        GIMarshallingTests.double_in(Number(self.MAX))

        self.assertRaises(TypeError, GIMarshallingTests.double_in, "self.MAX")

    def test_double_out(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.double_out())

    def test_double_inout(self):
        self.assertAlmostEqual(self.MIN, GIMarshallingTests.double_inout(Number(self.MAX)))


@unittest.skipUnless(GIMarshallingTests, "")
class TestGType(unittest.TestCase):

    def test_gtype_name(self):
        self.assertEqual("void", GObject.TYPE_NONE.name)
        self.assertEqual("gchararray", GObject.TYPE_STRING.name)

        def check_readonly(gtype):
            gtype.name = "foo"

        self.assertRaises(AttributeError, check_readonly, GObject.TYPE_NONE)
        self.assertRaises(AttributeError, check_readonly, GObject.TYPE_STRING)

    def test_gtype_return(self):
        self.assertEqual(GObject.TYPE_NONE, GIMarshallingTests.gtype_return())
        self.assertEqual(GObject.TYPE_STRING, GIMarshallingTests.gtype_string_return())

    def test_gtype_in(self):
        GIMarshallingTests.gtype_in(GObject.TYPE_NONE)
        GIMarshallingTests.gtype_string_in(GObject.TYPE_STRING)
        self.assertRaises(TypeError, GIMarshallingTests.gtype_in, "foo")
        self.assertRaises(TypeError, GIMarshallingTests.gtype_string_in, "foo")

    def test_gtype_out(self):
        self.assertEqual(GObject.TYPE_NONE, GIMarshallingTests.gtype_out())
        self.assertEqual(GObject.TYPE_STRING, GIMarshallingTests.gtype_string_out())

    def test_gtype_inout(self):
        self.assertEqual(GObject.TYPE_INT, GIMarshallingTests.gtype_inout(GObject.TYPE_NONE))


@unittest.skipUnless(GIMarshallingTests, "")
class TestPointer(unittest.TestCase):
    def test_pointer_in_return(self):
        self.assertEqual(GIMarshallingTests.pointer_in_return(42), 42)


@unittest.skipUnless(GIMarshallingTests, "")
class TestDir(unittest.TestCase):
    def test_members_list(self):
        list = dir(GIMarshallingTests)
        self.assertTrue('OverridesStruct' in list)
        self.assertTrue('BoxedStruct' in list)
        self.assertTrue('OVERRIDES_CONSTANT' in list)
        self.assertTrue('GEnum' in list)
        self.assertTrue('int32_return_max' in list)

    def test_modules_list(self):
        import gi.repository
        list = dir(gi.repository)
        self.assertTrue('GIMarshallingTests' in list)

        # FIXME: test to see if a module which was not imported is in the list
        #        we should be listing every typelib we find, not just the ones
        #        which are imported
        #
        #        to test this I recommend we compile a fake module which
        #        our tests would never import and check to see if it is
        #        in the list:
        #
        # self.assertTrue('DoNotImportDummyTests' in list)


@unittest.skipUnless(GIMarshallingTests, "")
class TestGObject(unittest.TestCase):

    def test_object(self):
        self.assertTrue(issubclass(GIMarshallingTests.Object, GObject.GObject))

        object_ = GIMarshallingTests.Object()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_new(self):
        object_ = GIMarshallingTests.Object.new(42)
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    @unittest.skip("FIXME")
    def test_object_int(self):
        object_ = GIMarshallingTests.Object(int=42)
        self.assertEqual(object_.int_, 42)
# FIXME: Don't work yet.
#        object_.int_ = 0
#        self.assertEqual(object_.int_, 0)

    def test_object_static_method(self):
        GIMarshallingTests.Object.static_method()

    def test_object_method(self):
        GIMarshallingTests.Object(int=42).method()
        self.assertRaises(TypeError, GIMarshallingTests.Object.method, GObject.GObject())
        self.assertRaises(TypeError, GIMarshallingTests.Object.method)

    def test_sub_object(self):
        self.assertTrue(issubclass(GIMarshallingTests.SubObject, GIMarshallingTests.Object))

        object_ = GIMarshallingTests.SubObject()
        self.assertTrue(isinstance(object_, GIMarshallingTests.SubObject))

    def test_sub_object_static_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.static_method()

    def test_sub_object_method(self):
        object_ = GIMarshallingTests.SubObject(int=42)
        object_.method()

    def test_sub_object_sub_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.sub_method()

    def test_sub_object_overwritten_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.overwritten_method()

        self.assertRaises(TypeError, GIMarshallingTests.SubObject.overwritten_method, GIMarshallingTests.Object())

    @unittest.skip("FIXME")
    def test_sub_object_int(self):
        object_ = GIMarshallingTests.SubObject()
        self.assertEqual(object_.int_, 0)
# FIXME: Don't work yet.
#        object_.int_ = 42
#        self.assertEqual(object_.int_, 42)

    def test_object_none_return(self):
        object_ = GIMarshallingTests.Object.none_return()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 2)

    def test_object_full_return(self):
        object_ = GIMarshallingTests.Object.full_return()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_none_in(self):
        object_ = GIMarshallingTests.Object(int=42)
        GIMarshallingTests.Object.none_in(object_)
        self.assertEqual(object_.__grefcount__, 1)

        object_ = GIMarshallingTests.SubObject(int=42)
        GIMarshallingTests.Object.none_in(object_)

        object_ = GObject.GObject()
        self.assertRaises(TypeError, GIMarshallingTests.Object.none_in, object_)

        self.assertRaises(TypeError, GIMarshallingTests.Object.none_in, None)

    def test_object_none_out(self):
        object_ = GIMarshallingTests.Object.none_out()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 2)

        new_object = GIMarshallingTests.Object.none_out()
        # FIXME?
        #self.assertTrue(new_object is object_)

    def test_object_full_out(self):
        object_ = GIMarshallingTests.Object.full_out()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_none_inout(self):
        object_ = GIMarshallingTests.Object(int=42)
        new_object = GIMarshallingTests.Object.none_inout(object_)

        self.assertTrue(isinstance(new_object, GIMarshallingTests.Object))

        self.assertFalse(object_ is new_object)

        self.assertEqual(object_.__grefcount__, 1)
        self.assertEqual(new_object.__grefcount__, 2)

        new_new_object = GIMarshallingTests.Object.none_inout(object_)
        # FIXME?
        #self.assertTrue(new_new_object is new_object)

        GIMarshallingTests.Object.none_inout(GIMarshallingTests.SubObject(int=42))

    def test_object_full_inout(self):
        object_ = GIMarshallingTests.Object(int=42)

        new_object = GIMarshallingTests.Object.full_inout(object_)

        self.assertTrue(isinstance(new_object, GIMarshallingTests.Object))

        self.assertFalse(object_ is new_object)

        self.assertEqual(object_.__grefcount__, 2)
        self.assertEqual(new_object.__grefcount__, 1)


@unittest.skipUnless(GIMarshallingTests, "")
class TestUtf8(unittest.TestCase):

    def test_utf8_none_return(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_none_return())

    def test_utf8_full_return(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_full_return())

    def test_utf8_none_in(self):
        GIMarshallingTests.utf8_none_in(CONSTANT_UTF8)
        if sys.version_info < (3, 0):
            GIMarshallingTests.utf8_none_in(PY2_UNICODE_UTF8)

        self.assertRaises(TypeError, GIMarshallingTests.utf8_none_in, CONSTANT_NUMBER)
        self.assertRaises(TypeError, GIMarshallingTests.utf8_none_in, None)

    def test_utf8_none_out(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_none_out())

    def test_utf8_full_out(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_full_out())

    def test_utf8_dangling_out(self):
        GIMarshallingTests.utf8_dangling_out()

    def test_utf8_none_inout(self):
        self.assertEqual("", GIMarshallingTests.utf8_none_inout(CONSTANT_UTF8))

    def test_utf8_full_inout(self):
        self.assertEqual("", GIMarshallingTests.utf8_full_inout(CONSTANT_UTF8))


class TestArray(unittest.TestCase):

    def test_array_fixed_int_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_int_return())

    def test_array_fixed_short_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_short_return())

    def test_array_fixed_int_in(self):
        GIMarshallingTests.array_fixed_int_in(Sequence([-1, 0, 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, Sequence([-1, '0', 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, None)

    def test_array_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_return())

    def test_array_return_etc(self):
        self.assertEqual(([5, 0, 1, 9], 14), GIMarshallingTests.array_return_etc(5, 9))

    def test_array_zero_terminated_return_null(self):
        self.assertEqual([], GIMarshallingTests.array_zero_terminated_return_null())


class TestProjectVersion(unittest.TestCase):
    def test_version_str(self):
        self.assertGreaterEqual(gi.__version__, "0.0.2")

    def test_version_info(self):
        self.assertEqual(len(gi.version_info), 3)
        self.assertGreaterEqual(gi.version_info, (0, 0, 2))

    def test_check_version(self):
        self.assertRaises(ValueError, gi.check_version, (99, 0, 0))
        self.assertRaises(ValueError, gi.check_version, "99.0.0")
        gi.check_version((0, 0, 2))
        gi.check_version("0.0.2")


@unittest.skipUnless(GIMarshallingTests, "")
class TestTimet(unittest.TestCase):

    def test_time_t_return(self):
        self.assertEqual(1234567890, GIMarshallingTests.time_t_return())

    def test_time_t_in(self):
        GIMarshallingTests.time_t_in(1234567890)
        self.assertRaises(TypeError, GIMarshallingTests.time_t_in, "hello")

    def test_time_t_out(self):
        self.assertEqual(1234567890, GIMarshallingTests.time_t_out())

    def test_time_t_inout(self):
        self.assertEqual(0, GIMarshallingTests.time_t_inout(1234567890))
