# coding=utf-8
# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# most tests here taken from pygobject "tests/test_everything.py"

import sys
import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

try:
    import cairo
    cairo
except ImportError:
    cairo = None

try:
    from gi.repository import Regress as Everything
    Everything
except ImportError:
    Everything = None

import tests
from tests import FIXME


def skipUnlessRegress(func):
    return unittest.skipUnless(Everything, "Regress missing")(func)


@skipUnlessRegress
class TestEverything(unittest.TestCase):

    @FIXME
    def test_cairo_context(self):
        context = Everything.test_cairo_context_full_return()
        self.assertTrue(isinstance(context, cairo.Context))

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
        context = cairo.Context(surface)
        Everything.test_cairo_context_none_in(context)

    @FIXME
    def test_cairo_surface(self):
        surface = Everything.test_cairo_surface_none_return()
        self.assertTrue(isinstance(surface, cairo.ImageSurface))
        self.assertTrue(isinstance(surface, cairo.Surface))
        self.assertEqual(surface.get_format(), cairo.FORMAT_ARGB32)
        self.assertEqual(surface.get_width(), 10)
        self.assertEqual(surface.get_height(), 10)

        surface = Everything.test_cairo_surface_full_return()
        self.assertTrue(isinstance(surface, cairo.ImageSurface))
        self.assertTrue(isinstance(surface, cairo.Surface))
        self.assertEqual(surface.get_format(), cairo.FORMAT_ARGB32)
        self.assertEqual(surface.get_width(), 10)
        self.assertEqual(surface.get_height(), 10)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
        Everything.test_cairo_surface_none_in(surface)

        surface = Everything.test_cairo_surface_full_out()
        self.assertTrue(isinstance(surface, cairo.ImageSurface))
        self.assertTrue(isinstance(surface, cairo.Surface))
        self.assertEqual(surface.get_format(), cairo.FORMAT_ARGB32)
        self.assertEqual(surface.get_width(), 10)
        self.assertEqual(surface.get_height(), 10)

    def test_bool(self):
        self.assertEqual(Everything.test_boolean(False), False)
        self.assertEqual(Everything.test_boolean(True), True)
        self.assertEqual(Everything.test_boolean('hello'), True)
        self.assertEqual(Everything.test_boolean(''), False)

        self.assertEqual(Everything.test_boolean_true(True), True)
        self.assertEqual(Everything.test_boolean_false(False), False)

    def test_int8(self):
        self.assertEqual(Everything.test_int8(GObject.G_MAXINT8),
                         GObject.G_MAXINT8)
        self.assertEqual(Everything.test_int8(GObject.G_MININT8),
                         GObject.G_MININT8)
        self.assertRaises(tests.GIOverflowError, Everything.test_int8, GObject.G_MAXINT8 + 1)

        self.assertEqual(Everything.test_uint8(GObject.G_MAXUINT8),
                         GObject.G_MAXUINT8)
        self.assertEqual(Everything.test_uint8(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint8, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint8, GObject.G_MAXUINT8 + 1)

    def test_int16(self):
        self.assertEqual(Everything.test_int16(GObject.G_MAXINT16),
                         GObject.G_MAXINT16)
        self.assertEqual(Everything.test_int16(GObject.G_MININT16),
                         GObject.G_MININT16)
        self.assertRaises(tests.GIOverflowError, Everything.test_int16, GObject.G_MAXINT16 + 1)

        self.assertEqual(Everything.test_uint16(GObject.G_MAXUINT16),
                         GObject.G_MAXUINT16)
        self.assertEqual(Everything.test_uint16(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint16, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint16, GObject.G_MAXUINT16 + 1)

    def test_int32(self):
        self.assertEqual(Everything.test_int32(GObject.G_MAXINT32),
                         GObject.G_MAXINT32)
        self.assertEqual(Everything.test_int32(GObject.G_MININT32),
                         GObject.G_MININT32)
        self.assertRaises(tests.GIOverflowError, Everything.test_int32, GObject.G_MAXINT32 + 1)

        self.assertEqual(Everything.test_uint32(GObject.G_MAXUINT32),
                         GObject.G_MAXUINT32)
        self.assertEqual(Everything.test_uint32(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint32, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint32, GObject.G_MAXUINT32 + 1)

    def test_int64(self):
        self.assertEqual(Everything.test_int64(GObject.G_MAXINT64),
                         GObject.G_MAXINT64)
        self.assertEqual(Everything.test_int64(GObject.G_MININT64),
                         GObject.G_MININT64)
        self.assertRaises(tests.GIOverflowError, Everything.test_int64, GObject.G_MAXINT64 + 1)

        self.assertEqual(Everything.test_uint64(GObject.G_MAXUINT64),
                         GObject.G_MAXUINT64)
        self.assertEqual(Everything.test_uint64(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint64, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint64, GObject.G_MAXUINT64 + 1)

    def test_int(self):
        self.assertEqual(Everything.test_int(GObject.G_MAXINT),
                         GObject.G_MAXINT)
        self.assertEqual(Everything.test_int(GObject.G_MININT),
                         GObject.G_MININT)
        self.assertRaises(tests.GIOverflowError, Everything.test_int, GObject.G_MAXINT + 1)

        self.assertEqual(Everything.test_uint(GObject.G_MAXUINT),
                         GObject.G_MAXUINT)
        self.assertEqual(Everything.test_uint(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_uint, GObject.G_MAXUINT + 1)

    def test_short(self):
        self.assertEqual(Everything.test_short(GObject.G_MAXSHORT),
                         GObject.G_MAXSHORT)
        self.assertEqual(Everything.test_short(GObject.G_MINSHORT),
                         GObject.G_MINSHORT)
        self.assertRaises(tests.GIOverflowError, Everything.test_short, GObject.G_MAXSHORT + 1)

        self.assertEqual(Everything.test_ushort(GObject.G_MAXUSHORT),
                         GObject.G_MAXUSHORT)
        self.assertEqual(Everything.test_ushort(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_ushort, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_ushort, GObject.G_MAXUSHORT + 1)

    def test_long(self):
        self.assertEqual(Everything.test_long(GObject.G_MAXLONG),
                         GObject.G_MAXLONG)
        self.assertEqual(Everything.test_long(GObject.G_MINLONG),
                         GObject.G_MINLONG)
        self.assertRaises(tests.GIOverflowError, Everything.test_long, GObject.G_MAXLONG + 1)

        self.assertEqual(Everything.test_ulong(GObject.G_MAXULONG),
                         GObject.G_MAXULONG)
        self.assertEqual(Everything.test_ulong(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_ulong, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_ulong, GObject.G_MAXULONG + 1)

    @unittest.skipUnless(hasattr(GObject, "G_MINSSIZE"), "too old gi")
    def test_size(self):
        self.assertEqual(Everything.test_ssize(GObject.G_MAXSSIZE),
                         GObject.G_MAXSSIZE)
        self.assertEqual(Everything.test_ssize(GObject.G_MINSSIZE),
                         GObject.G_MINSSIZE)
        self.assertRaises(tests.GIOverflowError, Everything.test_ssize, GObject.G_MAXSSIZE + 1)

        self.assertEqual(Everything.test_size(GObject.G_MAXSIZE),
                         GObject.G_MAXSIZE)
        self.assertEqual(Everything.test_size(0), 0)
        self.assertRaises(tests.GIOverflowError, Everything.test_size, -1)
        self.assertRaises(tests.GIOverflowError, Everything.test_size, GObject.G_MAXSIZE + 1)

    def test_timet(self):
        self.assertEqual(Everything.test_timet(42), 42)
        self.assertRaises(tests.GIOverflowError, Everything.test_timet, GObject.G_MAXUINT64 + 1)

    @FIXME
    def test_unichar(self):
        self.assertEqual("c", Everything.test_unichar("c"))

        if sys.version_info < (3, 0):
            self.assertEqual(UNICHAR, Everything.test_unichar(PY2_UNICODE_UNICHAR))
        self.assertEqual(UNICHAR, Everything.test_unichar(UNICHAR))
        self.assertRaises(TypeError, Everything.test_unichar, "")
        self.assertRaises(TypeError, Everything.test_unichar, "morethanonechar")

    def test_float(self):
        self.assertEqual(Everything.test_float(GObject.G_MAXFLOAT),
                         GObject.G_MAXFLOAT)
        self.assertEqual(Everything.test_float(GObject.G_MINFLOAT),
                         GObject.G_MINFLOAT)
        self.assertRaises(tests.GIOverflowError, Everything.test_float, GObject.G_MAXFLOAT * 2)

    def test_double(self):
        self.assertEqual(Everything.test_double(GObject.G_MAXDOUBLE),
                         GObject.G_MAXDOUBLE)
        self.assertEqual(Everything.test_double(GObject.G_MINDOUBLE),
                         GObject.G_MINDOUBLE)

        (two, three) = Everything.test_multi_double_args(2.5)
        self.assertAlmostEqual(two, 5.0)
        self.assertAlmostEqual(three, 7.5)

    @FIXME
    def test_value(self):
        self.assertEqual(Everything.test_int_value_arg(GObject.G_MAXINT), GObject.G_MAXINT)
        self.assertEqual(Everything.test_value_return(GObject.G_MAXINT), GObject.G_MAXINT)

    @FIXME
    def test_variant(self):
        v = Everything.test_gvariant_i()
        self.assertEqual(v.get_type_string(), 'i')
        self.assertEqual(v.get_int32(), 1)

        v = Everything.test_gvariant_s()
        self.assertEqual(v.get_type_string(), 's')
        self.assertEqual(v.get_string(), 'one')

        v = Everything.test_gvariant_v()
        self.assertEqual(v.get_type_string(), 'v')
        vi = v.get_variant()
        self.assertEqual(vi.get_type_string(), 's')
        self.assertEqual(vi.get_string(), 'contents')

        v = Everything.test_gvariant_as()
        self.assertEqual(v.get_type_string(), 'as')
        self.assertEqual(v.get_strv(), ['one', 'two', 'three'])

        v = Everything.test_gvariant_asv()
        self.assertEqual(v.get_type_string(), 'a{sv}')
        self.assertEqual(v.lookup_value('nosuchkey', None), None)
        name = v.lookup_value('name', None)
        self.assertEqual(name.get_string(), 'foo')
        timeout = v.lookup_value('timeout', None)
        self.assertEqual(timeout.get_int32(), 10)

    @FIXME
    def test_string(self):
        const_str = b'const \xe2\x99\xa5 utf8'
        if sys.version_info >= (3, 0):
            const_str = const_str.decode('UTF-8')
        noconst_str = 'non' + const_str

        self.assertEqual(Everything.test_utf8_const_return(), const_str)
        self.assertEqual(Everything.test_utf8_nonconst_return(), noconst_str)
        self.assertEqual(Everything.test_utf8_out(), noconst_str)

        Everything.test_utf8_const_in(const_str)
        self.assertEqual(Everything.test_utf8_inout(const_str), noconst_str)

        self.assertEqual(Everything.test_filename_return(), ['åäö', '/etc/fstab'])

        # returns g_utf8_strlen() in out argument
        self.assertEqual(Everything.test_int_out_utf8(''), 0)
        self.assertEqual(Everything.test_int_out_utf8('hello world'), 11)
        self.assertEqual(Everything.test_int_out_utf8('åäö'), 3)

        self.assertEqual(Everything.test_utf8_out_out(), ('first', 'second'))
        self.assertEqual(Everything.test_utf8_out_nonconst_return(), ('first', 'second'))

    def test_enum(self):
        self.assertEqual(Everything.test_enum_param(Everything.TestEnum.VALUE1), 'value1')
        self.assertEqual(Everything.test_enum_param(Everything.TestEnum.VALUE3), 'value3')
        self.assertRaises(TypeError, Everything.test_enum_param, 'hello')

    @FIXME
    def test_enum_unsigned(self):
        self.assertEqual(Everything.test_unsigned_enum_param(Everything.TestEnumUnsigned.VALUE1), 'value1')
        self.assertEqual(Everything.test_unsigned_enum_param(Everything.TestEnumUnsigned.VALUE3), 'value3')
        self.assertRaises(TypeError, Everything.test_unsigned_enum_param, 'hello')

    def test_flags(self):
        result = Everything.global_get_flags_out()
        # assert that it's not an int
        self.assertEqual(type(result), Everything.TestFlags)
        self.assertEqual(result, Everything.TestFlags.FLAG1 | Everything.TestFlags.FLAG3)

    @FIXME
    def test_floating(self):
        e = Everything.TestFloating()
        self.assertEqual(e.__grefcount__, 1)

        e = GObject.new(Everything.TestFloating)
        self.assertEqual(e.__grefcount__, 1)

        e = Everything.TestFloating.new()
        self.assertEqual(e.__grefcount__, 1)

@skipUnlessRegress
class TestNullableArgs(unittest.TestCase):
    @FIXME
    def test_in_nullable_hash(self):
        Everything.test_ghash_null_in(None)

    @FIXME
    def test_in_nullable_list(self):
        Everything.test_gslist_null_in(None)
        Everything.test_glist_null_in(None)
        Everything.test_gslist_null_in([])
        Everything.test_glist_null_in([])

    @FIXME
    def test_in_nullable_array(self):
        Everything.test_array_int_null_in(None)
        Everything.test_array_int_null_in([])

    def test_in_nullable_string(self):
        Everything.test_utf8_null_in(None)

    def test_in_nullable_object(self):
        Everything.func_obj_null_in(None)

    @FIXME
    def test_out_nullable_hash(self):
        self.assertEqual(None, Everything.test_ghash_null_out())

    @FIXME
    def test_out_nullable_list(self):
        self.assertEqual([], Everything.test_gslist_null_out())
        self.assertEqual([], Everything.test_glist_null_out())

    def test_out_nullable_array(self):
        self.assertEqual([], Everything.test_array_int_null_out())

    def test_out_nullable_string(self):
        self.assertEqual(None, Everything.test_utf8_null_out())

    def test_out_nullable_object(self):
        self.assertEqual(None, Everything.TestObj.null_out())


@skipUnlessRegress
class TestTortureProfile(unittest.TestCase):
    def test_torture_profile(self):
        import time
        total_time = 0
        print("")
        object_ = Everything.TestObj()
        sys.stdout.write("\ttorture test 1 (10000 iterations): ")

        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = object_.torture_signature_0(5000,
                                                    "Torture Test 1",
                                                    12345)

        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        sys.stdout.write("\ttorture test 2 (10000 iterations): ")

        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = Everything.TestObj().torture_signature_0(
                5000, "Torture Test 2", 12345)

        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        sys.stdout.write("\ttorture test 3 (10000 iterations): ")
        start_time = time.clock()
        for i in range(10000):
            try:
                (y, z, q) = object_.torture_signature_1(
                    5000, "Torture Test 3", 12345)
            except:
                pass
        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        # FIXME
        """sys.stdout.write("\ttorture test 4 (10000 iterations): ")

        def callback(userdata):
            pass

        userdata = [1, 2, 3, 4]
        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = Everything.test_torture_signature_2(
                5000, callback, userdata, "Torture Test 4", 12345)
        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time"""
        print("%f secs" % delta_time)
        print("\t====")
        print("\tTotal: %f sec" % total_time)


@skipUnlessRegress
class TestSignals(unittest.TestCase):
    def test_object_param_signal(self):
        obj = Everything.TestObj()

        def callback(obj, obj_param):
            self.assertEqual(obj_param.props.int, 3)
            self.assertGreater(obj_param.__grefcount__, 1)
            obj.called = True

        obj.called = False
        obj.connect('sig-with-obj', callback)
        obj.emit_sig_with_obj()
        self.assertTrue(obj.called)

    @FIXME
    def test_int64_param_from_py(self):
        obj = Everything.TestObj()

        def callback(obj, i):
            obj.callback_i = i
            return i

        obj.callback_i = None
        obj.connect('sig-with-int64-prop', callback)
        rv = obj.emit('sig-with-int64-prop', GObject.G_MAXINT64)
        self.assertEqual(rv, GObject.G_MAXINT64)
        self.assertEqual(obj.callback_i, GObject.G_MAXINT64)

    @FIXME
    def test_uint64_param_from_py(self):
        obj = Everything.TestObj()

        def callback(obj, i):
            obj.callback_i = i
            return i

        obj.callback_i = None
        obj.connect('sig-with-uint64-prop', callback)
        rv = obj.emit('sig-with-uint64-prop', GObject.G_MAXUINT64)
        self.assertEqual(rv, GObject.G_MAXUINT64)
        self.assertEqual(obj.callback_i, GObject.G_MAXUINT64)

    @FIXME
    def test_int64_param_from_c(self):
        obj = Everything.TestObj()

        def callback(obj, i):
            obj.callback_i = i
            return i

        obj.callback_i = None

        obj.connect('sig-with-int64-prop', callback)
        obj.emit_sig_with_int64()
        self.assertEqual(obj.callback_i, GObject.G_MAXINT64)

    @FIXME
    def test_uint64_param_from_c(self):
        obj = Everything.TestObj()

        def callback(obj, i):
            obj.callback_i = i
            return i

        obj.callback_i = None

        obj.connect('sig-with-uint64-prop', callback)
        obj.emit_sig_with_uint64()
        self.assertEqual(obj.callback_i, GObject.G_MAXUINT64)

    @FIXME
    def test_intarray_ret(self):
        obj = Everything.TestObj()

        def callback(obj, i):
            obj.callback_i = i
            return [i, i + 1]

        obj.callback_i = None

        try:
            obj.connect('sig-with-intarray-ret', callback)
        except TypeError as e:
            # compat with g-i 1.34.x
            if 'unknown signal' in str(e):
                return
            raise

        rv = obj.emit('sig-with-intarray-ret', 42)
        self.assertEqual(obj.callback_i, 42)
        self.assertEqual(type(rv), GLib.Array)
        self.assertEqual(rv.len, 2)
