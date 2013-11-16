# coding=utf-8
# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# most tests here taken from pygobject "tests/test_gi.py"

import tempfile
import shutil
import unittest
import os
import sys
from io import StringIO, BytesIO

import tests
from tests import _is_gi, skipUnlessGIVersion, skipIfGI, FIXME, skipIfPyPy

try:
    from gi.repository import GIMarshallingTests
except ImportError:
    GIMarshallingTests = None

import gi
from gi.repository import GObject, GLib, Gio

from compathelper import _bytes, _unicode

if sys.version_info < (3, 0):
    CONSTANT_UTF8 = "const \xe2\x99\xa5 utf8"
    PY2_UNICODE_UTF8 = unicode(CONSTANT_UTF8, 'UTF-8')
    CHAR_255 = '\xff'
else:
    CONSTANT_UTF8 = "const ♥ utf8"
    CHAR_255 = bytes([255])

CONSTANT_NUMBER = 42


def skipUnlessGIMarshallingTests(func):
    return unittest.skipUnless(GIMarshallingTests,
                               "GIMarshallingTests missing")(func)


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

    @skipUnlessGIMarshallingTests
    def test_constant_number(self):
        self.assertEqual(CONSTANT_NUMBER, GIMarshallingTests.CONSTANT_NUMBER)

    @unittest.skipUnless(hasattr(GLib, "MAXINT32"), "too old gi")
    def test_min_max_int(self):
        self.assertEqual(GLib.MAXINT32, 2 ** 31 - 1)
        self.assertEqual(GLib.MININT32, -2 ** 31)
        self.assertEqual(GLib.MAXUINT32, 2 ** 32 - 1)

        self.assertEqual(GLib.MAXINT64, 2 ** 63 - 1)
        self.assertEqual(GLib.MININT64, -2 ** 63)
        self.assertEqual(GLib.MAXUINT64, 2 ** 64 - 1)


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int8_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int8_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int8_in_max, "self.MAX")

    def test_int8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int8_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int8_out_min())

    def test_int8_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int8_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int8_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestUInt8(unittest.TestCase):

    MAX = GObject.G_MAXUINT8

    def test_uint8_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_return())

    def test_uint8_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint8_in(number)
        GIMarshallingTests.uint8_in(CHAR_255)

        number.value += 1
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint8_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint8_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint8_in, "self.MAX")

    def test_uint8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_out())

    def test_uint8_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint8_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int16_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int16_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int16_in_max, "self.MAX")

    def test_int16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int16_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int16_out_min())

    def test_int16_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int16_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int16_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestUInt16(unittest.TestCase):

    MAX = GObject.G_MAXUINT16

    def test_uint16_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_return())

    def test_uint16_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint16_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint16_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint16_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint16_in, "self.MAX")

    def test_uint16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_out())

    def test_uint16_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint16_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int32_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int32_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int32_in_max, "self.MAX")

    def test_int32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int32_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int32_out_min())

    def test_int32_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int32_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int32_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestUInt32(unittest.TestCase):

    MAX = GObject.G_MAXUINT32

    def test_uint32_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_return())

    def test_uint32_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint32_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint32_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint32_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint32_in, "self.MAX")

    def test_uint32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_out())

    def test_uint32_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint32_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int64_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int64_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int64_in_max, "self.MAX")

    def test_int64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int64_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int64_out_min())

    def test_int64_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int64_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int64_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestUInt64(unittest.TestCase):

    MAX = 2 ** 64 - 1

    def test_uint64_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_return())

    def test_uint64_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint64_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint64_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint64_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint64_in, "self.MAX")

    def test_uint64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_out())

    def test_uint64_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint64_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.short_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.short_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.short_in_max, "self.MAX")

    def test_short_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.short_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.short_out_min())

    def test_short_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.short_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.short_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestUShort(unittest.TestCase):

    MAX = GObject.G_MAXUSHORT

    def test_ushort_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_return())

    def test_ushort_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ushort_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ushort_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ushort_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ushort_in, "self.MAX")

    def test_ushort_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_out())

    def test_ushort_inout(self):
        self.assertEqual(0, GIMarshallingTests.ushort_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.int_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int_in_max, "self.MAX")

    def test_int_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int_out_min())

    def test_int_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int_inout_min_max(Number(self.MIN)))
        self.assertRaises(TypeError, GIMarshallingTests.int_inout_min_max, Number(self.MIN), CONSTANT_NUMBER)


@skipUnlessGIMarshallingTests
class TestUInt(unittest.TestCase):

    MAX = GObject.G_MAXUINT

    def test_uint_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_return())

    def test_uint_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.uint_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint_in, "self.MAX")

    def test_uint_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_out())

    def test_uint_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.long_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.long_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.long_in_max, "self.MAX")

    def test_long_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.long_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.long_out_min())

    def test_long_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.long_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.long_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestULong(unittest.TestCase):

    MAX = GObject.G_MAXULONG

    def test_ulong_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_return())

    def test_ulong_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ulong_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ulong_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ulong_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ulong_in, "self.MAX")

    def test_ulong_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_out())

    def test_ulong_inout(self):
        self.assertEqual(0, GIMarshallingTests.ulong_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ssize_in_max, max)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.ssize_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.ssize_in_max, "self.MAX")

    def test_ssize_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_out_min())

    def test_ssize_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_inout_min_max(Number(self.MIN)))


@skipUnlessGIMarshallingTests
class TestSize(unittest.TestCase):

    MAX = GObject.G_MAXULONG

    def test_size_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_return())

    def test_size_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.size_in(number)

        number.value += 1

        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.size_in, number)
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.size_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.size_in, "self.MAX")

    def test_size_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_out())

    def test_size_inout(self):
        self.assertEqual(0, GIMarshallingTests.size_inout(Number(self.MAX)))


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
class TestCallbacks(unittest.TestCase):
    def test_return_value_only(self):
        def cb():
            return 5
        self.assertEqual(GIMarshallingTests.callback_return_value_only(cb), 5)


@skipUnlessGIMarshallingTests
class TestPointer(unittest.TestCase):
    def test_pointer_in_return(self):
        self.assertEqual(GIMarshallingTests.pointer_in_return(42), 42)


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
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

    @FIXME
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

    @FIXME
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


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
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

    def test_array_fixed_short_in(self):
        GIMarshallingTests.array_fixed_short_in(Sequence([-1, 0, 1, 2]))

    def test_array_fixed_out(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_out())

    def test_array_fixed_inout(self):
        self.assertEqual([2, 1, 0, -1], GIMarshallingTests.array_fixed_inout([-1, 0, 1, 2]))

    def test_array_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_return())

    def test_array_return_etc(self):
        self.assertEqual(([5, 0, 1, 9], 14), GIMarshallingTests.array_return_etc(5, 9))

    def test_array_in(self):
        GIMarshallingTests.array_in(Sequence([-1, 0, 1, 2]))
        GIMarshallingTests.array_in_guint64_len(Sequence([-1, 0, 1, 2]))
        GIMarshallingTests.array_in_guint8_len(Sequence([-1, 0, 1, 2]))

    def test_array_in_len_before(self):
        GIMarshallingTests.array_in_len_before(Sequence([-1, 0, 1, 2]))

    def test_array_string_in(self):
        GIMarshallingTests.array_string_in(['foo', 'bar'])

    @skipUnlessGIVersion(3, 4)
    def test_array_in_len_zero_terminated(self):
        GIMarshallingTests.array_in_len_zero_terminated(Sequence([-1, 0, 1, 2]))

    def test_array_uint8_in(self):
        GIMarshallingTests.array_uint8_in(Sequence([97, 98, 99, 100]))
        GIMarshallingTests.array_uint8_in(_bytes("abcd"))

    def test_array_string_in(self):
        GIMarshallingTests.array_string_in(['foo', 'bar'])

    def test_array_out(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_out())

    def test_array_out_etc(self):
        self.assertEqual(([-5, 0, 1, 9], 4), GIMarshallingTests.array_out_etc(-5, 9))

    def test_array_inout(self):
        self.assertEqual([-2, -1, 0, 1, 2], GIMarshallingTests.array_inout(Sequence([-1, 0, 1, 2])))

    def test_array_inout_etc(self):
        self.assertEqual(([-5, -1, 0, 1, 9], 4),
                         GIMarshallingTests.array_inout_etc(-5, Sequence([-1, 0, 1, 2]), 9))

    def test_method_array_in(self):
        object_ = GIMarshallingTests.Object()
        object_.method_array_in(Sequence([-1, 0, 1, 2]))

    def test_method_array_out(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-1, 0, 1, 2], object_.method_array_out())

    def test_method_array_inout(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-2, -1, 0, 1, 2], object_.method_array_inout(Sequence([-1, 0, 1, 2])))

    def test_method_array_return(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-1, 0, 1, 2], object_.method_array_return())

    def test_array_enum_in(self):
        GIMarshallingTests.array_enum_in([GIMarshallingTests.Enum.VALUE1,
                                          GIMarshallingTests.Enum.VALUE2,
                                          GIMarshallingTests.Enum.VALUE3])

    def test_array_boxed_struct_in(self):
        struct1 = GIMarshallingTests.BoxedStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.BoxedStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.BoxedStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_struct_in([struct1, struct2, struct3])

    @FIXME
    def test_array_boxed_struct_value_in(self):
        struct1 = GIMarshallingTests.BoxedStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.BoxedStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.BoxedStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_struct_value_in([struct1, struct2, struct3])

    @FIXME
    def test_array_boxed_struct_take_in(self):
        struct1 = GIMarshallingTests.BoxedStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.BoxedStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.BoxedStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_struct_take_in([struct1, struct2, struct3])

        self.assertEqual(1, struct1.long_)

    @FIXME
    def test_array_boxed_struct_return(self):
        (struct1, struct2, struct3) = GIMarshallingTests.array_zero_terminated_return_struct()
        self.assertEqual(GIMarshallingTests.BoxedStruct, type(struct1))
        self.assertEqual(GIMarshallingTests.BoxedStruct, type(struct2))
        self.assertEqual(GIMarshallingTests.BoxedStruct, type(struct3))
        self.assertEqual(42, struct1.long_)
        self.assertEqual(43, struct2.long_)
        self.assertEqual(44, struct3.long_)

    @FIXME
    def test_array_simple_struct_in(self):
        struct1 = GIMarshallingTests.SimpleStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.SimpleStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.SimpleStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_simple_struct_in([struct1, struct2, struct3])

    @FIXME
    def test_array_multi_array_key_value_in(self):
        GIMarshallingTests.multi_array_key_value_in(["one", "two", "three"],
                                                    [1, 2, 3])

    def test_array_in_nonzero_nonlen(self):
        GIMarshallingTests.array_in_nonzero_nonlen(1, b'abcd')

    @FIXME
    def test_array_fixed_out_struct(self):
        struct1, struct2 = GIMarshallingTests.array_fixed_out_struct()

        self.assertEqual(7, struct1.long_)
        self.assertEqual(6, struct1.int8)
        self.assertEqual(6, struct2.long_)
        self.assertEqual(7, struct2.int8)

    def test_array_zero_terminated_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.array_zero_terminated_return())

    def test_array_zero_terminated_return_null(self):
        self.assertEqual([], GIMarshallingTests.array_zero_terminated_return_null())

    def test_array_zero_terminated_in(self):
        GIMarshallingTests.array_zero_terminated_in(Sequence(['0', '1', '2']))

    def test_array_zero_terminated_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.array_zero_terminated_out())

    def test_array_zero_terminated_inout(self):
        self.assertEqual(['-1', '0', '1', '2'], GIMarshallingTests.array_zero_terminated_inout(['0', '1', '2']))

    def test_init_function(self):
        self.assertEqual((True, []), GIMarshallingTests.init_function([]))
        self.assertEqual((True, []), GIMarshallingTests.init_function(['hello']))
        self.assertEqual((True, ['hello']),
                         GIMarshallingTests.init_function(['hello', 'world']))


@skipUnlessGIMarshallingTests
class TestPGI(unittest.TestCase):
    def test_array_type_checks(self):
        self.assertRaises(tests.GIOverflowError, GIMarshallingTests.array_in_len_before,
                          [-1, 0, 1, 2 + 2**32])

        self.assertRaises(TypeError, GIMarshallingTests.array_in_len_before,
                          [-1, 0, None, 2])


class TestProjectVersion(unittest.TestCase):
    @skipUnlessGIVersion(3, 4)
    def test_version_str(self):
        self.assertGreaterEqual(gi.__version__, "0.0.2")

    @skipUnlessGIVersion(3, 4)
    def test_version_info(self):
        self.assertTrue(len(gi.version_info) >= 3)
        self.assertGreaterEqual(gi.version_info, (0, 0, 2))

    @skipUnlessGIVersion(3, 4)
    def test_check_version(self):
        self.assertRaises(ValueError, gi.check_version, (99, 0, 0))
        self.assertRaises(ValueError, gi.check_version, "99.0.0")
        gi.check_version((0, 0, 2))
        gi.check_version("0.0.2")


@skipUnlessGIMarshallingTests
class TestEnum(unittest.TestCase):
    def test_enum(self):
        self.assertTrue(issubclass(GIMarshallingTests.Enum, int))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE1, GIMarshallingTests.Enum))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE2, GIMarshallingTests.Enum))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE3, GIMarshallingTests.Enum))
        self.assertEqual(42, GIMarshallingTests.Enum.VALUE3)

    @FIXME("no gtype")
    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.Enum.VALUE1.value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.Enum.VALUE2.value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.Enum.VALUE3.value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.Enum.VALUE1.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE1')
        self.assertEqual(GIMarshallingTests.Enum.VALUE2.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE2')
        self.assertEqual(GIMarshallingTests.Enum.VALUE3.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE3')

    def test_enum_in(self):
        GIMarshallingTests.enum_in(GIMarshallingTests.Enum.VALUE3)
        GIMarshallingTests.enum_in(42)

        self.assertRaises(TypeError, GIMarshallingTests.enum_in, 43)
        self.assertRaises(TypeError, GIMarshallingTests.enum_in, 'GIMarshallingTests.Enum.VALUE3')

    def test_enum_return(self):
        enum = GIMarshallingTests.enum_returnv()
        self.assertTrue(isinstance(enum, GIMarshallingTests.Enum))
        self.assertEqual(enum, GIMarshallingTests.Enum.VALUE3)

    def test_enum_out(self):
        enum = GIMarshallingTests.enum_out()
        self.assertTrue(isinstance(enum, GIMarshallingTests.Enum))
        self.assertEqual(enum, GIMarshallingTests.Enum.VALUE3)

    def test_enum_inout(self):
        enum = GIMarshallingTests.enum_inout(GIMarshallingTests.Enum.VALUE3)
        self.assertTrue(isinstance(enum, GIMarshallingTests.Enum))
        self.assertEqual(enum, GIMarshallingTests.Enum.VALUE1)

    def test_enum_second(self):
        # check for the bug where different non-gtype enums share the same class
        self.assertNotEqual(GIMarshallingTests.Enum, GIMarshallingTests.SecondEnum)

        # check that values are not being shared between different enums
        self.assertTrue(hasattr(GIMarshallingTests.SecondEnum, "SECONDVALUE1"))
        self.assertRaises(AttributeError, getattr, GIMarshallingTests.Enum, "SECONDVALUE1")
        self.assertTrue(hasattr(GIMarshallingTests.Enum, "VALUE1"))
        self.assertRaises(AttributeError, getattr, GIMarshallingTests.SecondEnum, "VALUE1")

    @unittest.skip("no gtype")
    def test_enum_gtype_name_is_namespaced(self):
        self.assertEqual(GIMarshallingTests.Enum.__gtype__.name,
                         'GIMarshallingTestsEnum')


@skipUnlessGIMarshallingTests
class TestGEnum(unittest.TestCase):
    def test_genum(self):
        self.assertTrue(issubclass(GIMarshallingTests.GEnum, GObject.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE1, GIMarshallingTests.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE2, GIMarshallingTests.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE3, GIMarshallingTests.GEnum))
        self.assertEqual(42, GIMarshallingTests.GEnum.VALUE3)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.GEnum.VALUE1.value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE2.value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE3.value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.GEnum.VALUE1.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE1')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE2.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE2')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE3.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE3')


    def test_genum_in(self):
        GIMarshallingTests.genum_in(GIMarshallingTests.GEnum.VALUE3)
        GIMarshallingTests.genum_in(42)

        self.assertRaises(TypeError, GIMarshallingTests.genum_in, 43)
        self.assertRaises(TypeError, GIMarshallingTests.genum_in, 'GIMarshallingTests.GEnum.VALUE3')

    def test_genum_return(self):
        genum = GIMarshallingTests.genum_returnv()
        self.assertTrue(isinstance(genum, GIMarshallingTests.GEnum))
        self.assertEqual(genum, GIMarshallingTests.GEnum.VALUE3)

    def test_genum_out(self):
        genum = GIMarshallingTests.genum_out()
        self.assertTrue(isinstance(genum, GIMarshallingTests.GEnum))
        self.assertEqual(genum, GIMarshallingTests.GEnum.VALUE3)

    def test_genum_inout(self):
        genum = GIMarshallingTests.genum_inout(GIMarshallingTests.GEnum.VALUE3)
        self.assertTrue(isinstance(genum, GIMarshallingTests.GEnum))
        self.assertEqual(genum, GIMarshallingTests.GEnum.VALUE1)


@skipUnlessGIMarshallingTests
class TestGFlags(unittest.TestCase):

    def test_flags(self):
        self.assertTrue(issubclass(GIMarshallingTests.Flags, GObject.GFlags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE1, GIMarshallingTests.Flags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE2, GIMarshallingTests.Flags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE3, GIMarshallingTests.Flags))
        # __or__() operation should still return an instance, not an int.
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE1 | GIMarshallingTests.Flags.VALUE2,
                                   GIMarshallingTests.Flags))
        self.assertEqual(1 << 1, GIMarshallingTests.Flags.VALUE2)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.Flags.VALUE1.first_value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.Flags.VALUE2.first_value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.Flags.VALUE3.first_value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.Flags.VALUE1.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE1')
        self.assertEqual(GIMarshallingTests.Flags.VALUE2.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE2')
        self.assertEqual(GIMarshallingTests.Flags.VALUE3.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE3')

    def test_flags_in(self):
        GIMarshallingTests.flags_in(GIMarshallingTests.Flags.VALUE2)
        # result of __or__() operation should still be valid instance, not an int.
        GIMarshallingTests.flags_in(GIMarshallingTests.Flags.VALUE2 | GIMarshallingTests.Flags.VALUE2)
        GIMarshallingTests.flags_in_zero(Number(0))

        self.assertRaises(TypeError, GIMarshallingTests.flags_in, 1 << 1)
        self.assertRaises(TypeError, GIMarshallingTests.flags_in, 'GIMarshallingTests.Flags.VALUE2')

    def test_flags_return(self):
        flags = GIMarshallingTests.flags_returnv()
        self.assertTrue(isinstance(flags, GIMarshallingTests.Flags))
        self.assertEqual(flags, GIMarshallingTests.Flags.VALUE2)

    def test_flags_out(self):
        flags = GIMarshallingTests.flags_out()
        self.assertTrue(isinstance(flags, GIMarshallingTests.Flags))
        self.assertEqual(flags, GIMarshallingTests.Flags.VALUE2)

    def test_flags_inout(self):
        flags = GIMarshallingTests.flags_inout(GIMarshallingTests.Flags.VALUE2)
        self.assertTrue(isinstance(flags, GIMarshallingTests.Flags))
        self.assertEqual(flags, GIMarshallingTests.Flags.VALUE1)


@skipUnlessGIMarshallingTests
class TestNoTypeFlags(unittest.TestCase):

    def test_flags(self):
        self.assertTrue(issubclass(GIMarshallingTests.NoTypeFlags, GObject.GFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE1, GIMarshallingTests.NoTypeFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE2, GIMarshallingTests.NoTypeFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE3, GIMarshallingTests.NoTypeFlags))
        # __or__() operation should still return an instance, not an int.
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE1 | GIMarshallingTests.NoTypeFlags.VALUE2,
                                   GIMarshallingTests.NoTypeFlags))
        self.assertEqual(1 << 1, GIMarshallingTests.NoTypeFlags.VALUE2)

    @unittest.skip("no gtype")
    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE1.first_value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE2.first_value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE3.first_value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE1.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE1')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE2.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE2')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE3.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE3')

    def test_flags_in(self):
        GIMarshallingTests.no_type_flags_in(GIMarshallingTests.NoTypeFlags.VALUE2)
        GIMarshallingTests.no_type_flags_in(GIMarshallingTests.NoTypeFlags.VALUE2 | GIMarshallingTests.NoTypeFlags.VALUE2)
        GIMarshallingTests.no_type_flags_in_zero(Number(0))

        self.assertRaises(TypeError, GIMarshallingTests.no_type_flags_in, 1 << 1)
        self.assertRaises(TypeError, GIMarshallingTests.no_type_flags_in, 'GIMarshallingTests.NoTypeFlags.VALUE2')

    def test_flags_return(self):
        flags = GIMarshallingTests.no_type_flags_returnv()
        self.assertTrue(isinstance(flags, GIMarshallingTests.NoTypeFlags))
        self.assertEqual(flags, GIMarshallingTests.NoTypeFlags.VALUE2)

    def test_flags_out(self):
        flags = GIMarshallingTests.no_type_flags_out()
        self.assertTrue(isinstance(flags, GIMarshallingTests.NoTypeFlags))
        self.assertEqual(flags, GIMarshallingTests.NoTypeFlags.VALUE2)

    def test_flags_inout(self):
        flags = GIMarshallingTests.no_type_flags_inout(GIMarshallingTests.NoTypeFlags.VALUE2)
        self.assertTrue(isinstance(flags, GIMarshallingTests.NoTypeFlags))
        self.assertEqual(flags, GIMarshallingTests.NoTypeFlags.VALUE1)

    @unittest.skip("no gtype")
    def test_flags_gtype_name_is_namespaced(self):
        self.assertEqual(GIMarshallingTests.NoTypeFlags.__gtype__.name,
                         'GIMarshallingTestsNoTypeFlags')


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
class TestMultiOutputArgs(unittest.TestCase):

    def test_int_out_out(self):
        self.assertEqual((6, 7), GIMarshallingTests.int_out_out())

    def test_int_return_out(self):
        self.assertEqual((6, 7), GIMarshallingTests.int_return_out())


@skipUnlessGIMarshallingTests
class TestGErrorException(unittest.TestCase):
    def test_gerror_exception(self):
        self.assertRaises(GObject.GError, GIMarshallingTests.gerror)
        try:
            GIMarshallingTests.gerror()
        except Exception:
            etype, e = sys.exc_info()[:2]
            self.assertEqual(e.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
            self.assertEqual(e.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
            self.assertEqual(e.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)


@skipUnlessGIMarshallingTests
class TestGErrorOut(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_gerror_out(self):
        error, debug = GIMarshallingTests.gerror_out()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)
        self.assertEqual(debug, GIMarshallingTests.CONSTANT_GERROR_DEBUG_MESSAGE)


@skipUnlessGIMarshallingTests
class TestGErrorOutTransferNone(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_gerror_out_transfer_none(self):
        error, debug = GIMarshallingTests.gerror_out_transfer_none()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)
        self.assertEqual(GIMarshallingTests.CONSTANT_GERROR_DEBUG_MESSAGE, debug)


@skipIfGI
@skipUnlessGIMarshallingTests
class TestInterfaces(unittest.TestCase):

    if GIMarshallingTests and not _is_gi:
        class TestInterfaceImpl(GObject.GObject, GIMarshallingTests.Interface):
            def __init__(self):
                GObject.GObject.__init__(self)
                self.val = None

            def do_test_int8_in(self, int8):
                self.val = int8

    def setUp(self):
        self.instance = self.TestInterfaceImpl()

    def test_wrapper(self):
        self.assertTrue(issubclass(GIMarshallingTests.Interface, GObject.GInterface))
        self.assertEqual(GIMarshallingTests.Interface.__gtype__.name, 'GIMarshallingTestsInterface')
        self.assertRaises(NotImplementedError, GIMarshallingTests.Interface)

    def test_implementation(self):
        self.assertTrue(issubclass(self.TestInterfaceImpl, GIMarshallingTests.Interface))
        self.assertTrue(isinstance(self.instance, GIMarshallingTests.Interface))

    @FIXME
    def test_int8_int(self):
        GIMarshallingTests.test_interface_test_int8_in(self.instance, 42)
        self.assertEqual(self.instance.val, 42)

    @FIXME
    def test_subclass(self):
        class TestInterfaceImplA(self.TestInterfaceImpl):
            pass

        class TestInterfaceImplB(TestInterfaceImplA):
            pass

        instance = TestInterfaceImplA()
        GIMarshallingTests.test_interface_test_int8_in(instance, 42)
        self.assertEqual(instance.val, 42)

    @FIXME
    def test_mro(self):
        # there was a problem with Python bailing out because of
        # http://en.wikipedia.org/wiki/Diamond_problem with interfaces,
        # which shouldn't really be a problem.

        class TestInterfaceImpl(GObject.GObject, GIMarshallingTests.Interface):
            pass

        class TestInterfaceImpl2(GIMarshallingTests.Interface,
                                 TestInterfaceImpl):
            pass

        class TestInterfaceImpl3(self.TestInterfaceImpl,
                                 GIMarshallingTests.Interface2):
            pass

    def test_type_mismatch(self):
        obj = GIMarshallingTests.Object()

        # wrong type for first argument: interface
        enum = Gio.File.new_for_path('.').enumerate_children(
            '', Gio.FileQueryInfoFlags.NONE, None)
        try:
            enum.next_file(obj)
            self.fail('call with wrong type argument unexpectedly succeeded')
        except TypeError as e:
            # should have argument name
            self.assertTrue('cancellable' in str(e), e)
            # should have expected type
            self.assertTrue('Cancellable' in str(e), e)
            # should have actual type
            self.assertTrue('Object' in str(e), e)

    @FIXME
    def test_type_mismatch2(self):
        # wrong type for self argument: interface
        try:
            Gio.FileEnumerator.next_file(obj, None)
            self.fail('call with wrong type argument unexpectedly succeeded')
        except TypeError as e:
            if sys.version_info < (3, 0):
                self.assertTrue('FileEnumerator' in str(e), e)
                self.assertTrue('Object' in str(e), e)
            else:
                # should have argument name
                self.assertTrue('self' in str(e), e)
                # should have expected type
                self.assertTrue('xpected Gio.FileEnumerator' in str(e), e)
                # should have actual type
                self.assertTrue('GIMarshallingTests.Object' in str(e), e)

        # wrong type for first argument: GObject
        var = GLib.Variant('s', 'mystring')
        action = Gio.SimpleAction.new('foo', var.get_type())
        try:
            action.activate(obj)
            self.fail('call with wrong type argument unexpectedly succeeded')
        except TypeError as e:
            # should have argument name
            self.assertTrue('parameter' in str(e), e)
            # should have expected type
            self.assertTrue('xpected GLib.Variant' in str(e), e)
            # should have actual type
            self.assertTrue('GIMarshallingTests.Object' in str(e), e)

        # wrong type for self argument: GObject
        try:
            Gio.SimpleAction.activate(obj, obj)
            self.fail('call with wrong type argument unexpectedly succeeded')
        except TypeError as e:
            if sys.version_info < (3, 0):
                self.assertTrue('SimpleAction' in str(e), e)
                self.assertTrue('Object' in str(e), e)
            else:
                # should have argument name
                self.assertTrue('self' in str(e), e)
                # should have expected type
                self.assertTrue('xpected Gio.Action' in str(e), e)
                # should have actual type
                self.assertTrue('GIMarshallingTests.Object' in str(e), e)


@skipUnlessGIMarshallingTests
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


@skipUnlessGIMarshallingTests
class TestGErrorReturn(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_return_gerror(self):
        error = GIMarshallingTests.gerror_return()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)


@skipUnlessGIMarshallingTests
class TestKeywordArgs(unittest.TestCase):

    def test_calling(self):
        kw_func = GIMarshallingTests.int_three_in_three_out

        self.assertEqual(kw_func(1, 2, 3), (1, 2, 3))
        self.assertEqual(kw_func(**{'a': 4, 'b': 5, 'c': 6}), (4, 5, 6))
        self.assertEqual(kw_func(1, **{'b': 7, 'c': 8}), (1, 7, 8))
        self.assertEqual(kw_func(1, 7, **{'c': 8}), (1, 7, 8))
        self.assertEqual(kw_func(1, c=8, **{'b': 7}), (1, 7, 8))
        self.assertEqual(kw_func(2, c=4, b=3), (2, 3, 4))
        self.assertEqual(kw_func(a=2, c=4, b=3), (2, 3, 4))

    def assertRaisesMessage(self, exception, message, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception:
            (e_type, e) = sys.exc_info()[:2]
            if message is not None:
                self.assertEqual(str(e), message)
        except:
            raise
        else:
            msg = "%s() did not raise %s" % (func.__name__, exception.__name__)
            raise AssertionError(msg)

    def test_type_errors(self):
        # test too few args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (1 given)",
                                 GIMarshallingTests.int_three_in_three_out, 1)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out, *())
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(), **{})
        if _is_gi:
            self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 non-keyword arguments (0 given)",
                                     GIMarshallingTests.int_three_in_three_out, *(), **{'c': 4})
        else:
            self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (1 given)",
                                     GIMarshallingTests.int_three_in_three_out, *(), **{'c': 4})

        # test too many args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (4 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(1, 2, 3, 4))
        if _is_gi:
            self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 non-keyword arguments (4 given)",
                                     GIMarshallingTests.int_three_in_three_out, *(1, 2, 3, 4), c=6)
        else:
            self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (5 given)",
                                     GIMarshallingTests.int_three_in_three_out, *(1, 2, 3, 4), c=6)

        # test too many keyword args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got multiple values for keyword argument 'a'",
                                 GIMarshallingTests.int_three_in_three_out, 1, 2, 3, **{'a': 4, 'b': 5})
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got an unexpected keyword argument 'd'",
                                 GIMarshallingTests.int_three_in_three_out, d=4)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got an unexpected keyword argument 'e'",
                                 GIMarshallingTests.int_three_in_three_out, **{'e': 2})

    def test_kwargs_are_not_modified(self):
        d = {'b': 2}
        d2 = d.copy()
        GIMarshallingTests.int_three_in_three_out(1, c=4, **d)
        self.assertEqual(d, d2)


@skipUnlessGIMarshallingTests
class TestPropertiesObject(unittest.TestCase):

    def setUp(self):
        self.obj = GIMarshallingTests.PropertiesObject()

    def test_boolean(self):
        self.assertEqual(self.obj.props.some_boolean, False)
        self.obj.props.some_boolean = True
        self.assertEqual(self.obj.props.some_boolean, True)

        obj = GIMarshallingTests.PropertiesObject(some_boolean=True)
        self.assertEqual(obj.props.some_boolean, True)


class TestKeywords(unittest.TestCase):
    @FIXME
    def test_method(self):
        # g_variant_print()
        v = GLib.Variant('i', 1)
        self.assertEqual(v.print_(False), '1')

    @skipUnlessGIVersion(3, 4)
    def test_function(self):
        # g_thread_yield()
        self.assertEqual(GLib.Thread.yield_(), None)

    @skipUnlessGIVersion(3, 4)
    def test_struct_method(self):
        # g_timer_continue()
        # we cannot currently instantiate GLib.Timer objects, so just ensure
        # the method exists
        self.assertTrue(callable(GLib.Timer.continue_))

    def test_uppercase(self):
        self.assertEqual(GLib.IOCondition.IN.value_nicks, ['in'])


@skipUnlessGIMarshallingTests
class TestModule(unittest.TestCase):
    def test_path(self):
        self.assertTrue(GIMarshallingTests.__path__.endswith('GIMarshallingTests-1.0.typelib'),
                        GIMarshallingTests.__path__)

    def test_str(self):
        self.assertTrue("'GIMarshallingTests' from '" in str(GIMarshallingTests),
                        str(GIMarshallingTests))

    @skipUnlessGIVersion(3, 4)
    def test_dir(self):
        _dir = dir(GIMarshallingTests)
        self.assertGreater(len(_dir), 10)

        self.assertTrue('SimpleStruct' in _dir)
        self.assertTrue('Interface2' in _dir)
        self.assertTrue('CONSTANT_GERROR_CODE' in _dir)
        self.assertTrue('array_zero_terminated_inout' in _dir)

        # assert that dir() does not contain garbage
        for item_name in _dir:
            item = getattr(GIMarshallingTests, item_name)
            self.assertTrue(hasattr(item, '__class__'))

    @skipUnlessGIVersion(3, 4)
    @skipIfPyPy("pypy gets confused by some __path__")
    def test_help(self):
        orig_stdout = sys.stdout
        try:
            if sys.version_info < (3, 0):
                sys.stdout = BytesIO()
            else:
                sys.stdout = StringIO()
            help(GIMarshallingTests)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = orig_stdout

        self.assertTrue('SimpleStruct' in output, output)
        self.assertTrue('Interface2' in output, output)
        self.assertTrue('method_array_inout' in output, output)


@skipUnlessGIMarshallingTests
class TestGStrv(unittest.TestCase):

    def test_gstrv_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gstrv_return())

    def test_gstrv_in(self):
        GIMarshallingTests.gstrv_in(Sequence(['0', '1', '2']))

    def test_gstrv_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gstrv_out())

    def test_gstrv_inout(self):
        self.assertEqual(['-1', '0', '1', '2'], GIMarshallingTests.gstrv_inout(['0', '1', '2']))
