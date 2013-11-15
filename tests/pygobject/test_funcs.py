# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import tests
from tests import skipUnlessGIVersion, skipIfGI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Pango
from pgi import _compat


class FuncsTest(unittest.TestCase):

    @skipIfGI
    def test_escape_name(self):
        self.failUnless(Pango.break_)
        self.failUnless(Pango.break_.__doc__.startswith("break_("))

    def test_basic(self):
        self.assertTrue("themes" in Gtk.rc_get_theme_dir())
        self.assertTrue(Gtk.rc_get_module_dir())
        self.assertEqual(Gtk.rc_get_default_files(), [])
        self.assertEqual(Gtk.get_current_event_time(), 0)

    def test_basic_argument(self):
        self.assertEqual(GLib.basename("/omg/foo/test"), "test")
        self.assertEqual(GLib.basename(u"/omg/foo/test"), "test")

    def test_return_guint(self):
        self.assertTrue(isinstance(Gtk.get_binary_age(),
                        _compat.integer_types))

    def test_return_misc(self):
        self.assertTrue(
            isinstance(Gtk.icon_size_register("foo", 1, 2),
                       _compat.integer_types))
        self.assertEqual(Gtk.icon_size_get_name(Gtk.IconSize.MENU),
                         "gtk-menu")

    def test_misc(self):
        b = Gtk.Button()
        self.assertEqual(b.get_relief(), Gtk.ReliefStyle.NORMAL)
        b.set_relief(Gtk.ReliefStyle.HALF)
        self.assertEqual(b.get_relief(), Gtk.ReliefStyle.HALF)

        b.set_label("foo")
        self.assertEqual(b.get_label(), "foo")

        self.assertFalse(b.get_use_stock())
        b.set_use_stock(True)
        self.assertTrue(b.get_use_stock())

        self.assertTrue(b.get_focus_on_click())

        b.set_alignment(0.25, 0.75)
        self.assertEqual(b.get_alignment(), (0.25, 0.75))

        b.set_use_stock([])
        self.assertFalse(b.get_use_stock())
        b.set_use_stock(3.4)
        self.assertTrue(b.get_use_stock())
        b.set_use_stock(b)
        self.assertTrue(b.get_use_stock())

        b.get_event_window()

    def test_return_object(self):
        b = Gtk.Button()
        f = Gtk.Frame()
        f.set_label_widget(b)
        self.assertTrue(isinstance(f.get_label_widget(), Gtk.Widget))
        self.assertTrue(isinstance(f.get_label_widget(), Gtk.Button))

    def test_misc_invalid(self):
        b = Gtk.Button()
        self.assertRaises(TypeError, b.set_label, 1)
        self.assertRaises(TypeError, b.set_label, [])
        self.assertRaises(TypeError, b.set_label, 3.4)
        self.assertRaises(TypeError, b.set_label, b)

        self.assertRaises(TypeError, b.set_relief, [])
        self.assertRaises(TypeError, b.set_relief, 3.4)
        self.assertRaises(TypeError, b.set_relief, b)

    def test_func_throws(self):
        builder = Gtk.Builder()
        self.assertRaises(GObject.GError, builder.add_from_file, "")

    def test_func_string_null(self):
        ag = Gtk.ActionGroup("foo")
        a = Gtk.Action("foo2", "bar", "blah", Gtk.STOCK_NEW)
        self.assertRaises(TypeError, ag.add_action_with_accel, a, 0)
        self.assertRaises(TypeError, ag.add_action_with_accel, a, [])
        ag.add_action_with_accel(a, None)
        b = Gtk.Action("foo3", "bar", "blah", Gtk.STOCK_NEW)
        ag.add_action_with_accel(b, "<ctrl>a")

    def test_pass_object(self):
        action = Gtk.RadioAction("", "", None, None, 0)
        self.assertRaises(TypeError, action.join_group, 1)
        self.assertRaises(TypeError, action.join_group, [])
        self.assertRaises(TypeError, action.join_group, 0)
        action.join_group(None)

        button = Gtk.Button()
        box = Gtk.Box()
        box.add(button)
        self.assertRaises(TypeError, box.add, None)

    def test_uint32_in_out(self):
        a = Gtk.Alignment()
        self.assertEqual(a.get_padding(), (0, 0, 0, 0))
        a.set_padding(1, 2, 3, 4)
        self.assertEqual(a.get_padding(), (1, 2, 3, 4))
        a.set_padding(1, 2, 3, 2**32-1)
        a.set_padding(1, 2, 3, _compat.long_type(4))
        a.set_padding(1, 2, 3, 1.9)
        self.assertEqual(a.get_padding(), (1, 2, 3, 1))
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, "")
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, "1")
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, [])
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, None)
        self.assertRaises(tests.GIOverflowError, a.set_padding, 1, 2, 3, -1)
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, 2+1j)
        self.assertRaises(tests.GIOverflowError, a.set_padding, 1, 2, 3, 2**32)

    def test_array_c_in(self):
        Gtk.ListStore().set_column_types([])

    def test_bool_return(self):
        a = Gtk.Action("", "", "", "")
        v = a.get_always_show_image()
        self.assertTrue(isinstance(v, bool))

    def test_double_in_out(self):
        a = Gtk.HSV()
        a.set_color(0.25, 0.5, 1)
        a.set_color(0.25, 0.5, _compat.long_type(1))
        a.set_color(0.25, 0.5, 0.75)
        a.set_color(0.25, 0.5, True)
        self.assertRaises(TypeError, a.set_color, 0, 0, "")
        self.assertRaises(TypeError, a.set_color, 0, 0, None)

        self.assertEqual(a.get_color(), (0.25, 0.5, 1))

    def test_double_return(self):
        a = Gtk.Adjustment()
        a.set_lower(2.25)
        self.assertEqual(a.get_lower(), 2.25)

    def test_flags_return(self):
        b = Gtk.Button()
        c = b.get_style_context()
        junction = c.get_junction_sides()
        self.assertTrue(isinstance(junction, Gtk.JunctionSides))

    def test_enum_return(self):
        b = Gtk.Button()
        c = b.get_style_context()
        direction = c.get_direction()
        self.assertTrue(isinstance(direction, Gtk.TextDirection))

    def test_value_boolean(self):
        v = GObject.Value()
        v.init(GObject.TYPE_BOOLEAN)
        v.set_boolean(True)
        self.assertEqual(v.get_boolean(), True)
        v.set_boolean(False)
        self.assertEqual(v.get_boolean(), False)
        v.set_boolean([])
        self.assertEqual(v.get_boolean(), False)
        v.set_boolean([1])
        self.assertEqual(v.get_boolean(), True)

    def test_value_char(self):
        v = GObject.Value()
        v.init(GObject.TYPE_CHAR)
        v.set_char(97)
        self.assertEqual(v.get_char(), 97)
        self.assertRaises(TypeError, v.set_char, u"a")
        self.assertRaises(TypeError, v.set_char, "ab")
        self.assertRaises(tests.GIOverflowError, v.set_char, 9999)
        v.set_char(103.5)
        self.assertEqual(v.get_char(), 103)

    def test_value_double(self):
        v = GObject.Value()
        v.init(GObject.TYPE_DOUBLE)
        v.set_double(42.50)
        self.assertEqual(v.get_double(), 42.50)
        self.assertRaises(TypeError, v.set_double, "a")

    def test_value_gtype(self):
        v = GObject.Value()
        v.init(GObject.TYPE_GTYPE)
        v.set_gtype(GObject.TYPE_DOUBLE)
        self.assertEqual(v.get_gtype(), GObject.TYPE_DOUBLE)

    def test_value_gtype_convert(self):
        v = GObject.Value()
        v.init(GObject.TYPE_GTYPE)
        v.set_gtype(str)
        self.assertEqual(v.get_gtype(), GObject.TYPE_STRING)
        v.set_gtype(int)
        self.assertEqual(v.get_gtype(), GObject.TYPE_INT)
        v.set_gtype(float)
        self.assertEqual(v.get_gtype(), GObject.TYPE_DOUBLE)
        v.set_gtype(bool)
        self.assertEqual(v.get_gtype(), GObject.TYPE_BOOLEAN)

    def test_value_float(self):
        v = GObject.Value()
        v.init(GObject.TYPE_FLOAT)
        v.set_float(42.50)
        self.assertEqual(v.get_float(), 42.50)
        v.set_float(42)
        self.assertEqual(v.get_float(), 42)
        self.assertRaises(TypeError, v.set_float, "a")
        self.assertRaises(TypeError, v.set_float, [])
        self.assertRaises(tests.GIOverflowError, v.set_float, 10**39)
        self.assertRaises(tests.GIOverflowError, v.set_float, -10**39)

    @skipUnlessGIVersion(3, 6)
    def test_value_float_inf(self):
        v = GObject.Value()
        v.init(GObject.TYPE_FLOAT)
        v.set_float(float("inf"))
        self.assertEqual(v.get_float(), float('inf'))
        v.set_float(float("-inf"))
        self.assertEqual(v.get_float(), float('-inf'))

    def test_value_int32(self):
        v = GObject.Value()
        v.init(GObject.TYPE_INT)
        v.set_int(2**31 - 1)
        v.set_int(-2**31)
        v.set_int(42.50)
        self.assertEqual(v.get_int(), 42)
        self.assertRaises(TypeError, v.set_int, "a")
        self.assertRaises(tests.GIOverflowError, v.set_int, 2**31)
        self.assertRaises(tests.GIOverflowError, v.set_int, -(2**31+1))

    def test_value_int64(self):
        v = GObject.Value()
        v.init(GObject.TYPE_INT64)
        v.set_int64(2**63 - 1)
        v.set_int64(-2**63)
        v.set_int64(42.50)
        self.assertEqual(v.get_int64(), 42)
        self.assertRaises(TypeError, v.set_int64, "a")
        self.assertRaises(tests.GIOverflowError, v.set_int64, 2**63)
        self.assertRaises(tests.GIOverflowError, v.set_int64, -(2**63+1))

    def test_value_long(self):
        v = GObject.Value()
        v.init(GObject.TYPE_LONG)
        v.set_long(GObject.G_MAXLONG)
        v.set_long(GObject.G_MINLONG)
        v.set_long(42.50)
        self.assertEqual(v.get_long(), 42)
        self.assertRaises(TypeError, v.set_long, "a")
        self.assertRaises(
            tests.GIOverflowError, v.set_long, GObject.G_MAXLONG + 1)
        self.assertRaises(
            tests.GIOverflowError, v.set_long, GObject.G_MINLONG - 1)

    def test_value_object(self):
        b = Gtk.Button()
        v = GObject.Value()
        v.init(GObject.TYPE_OBJECT)
        v.set_object(b)
        v.set_object(None)
        self.assertTrue(v.get_object() is None)
        v.set_object(b)
        self.assertEqual(v.get_object(), b)

    def test_value_uchar(self):
        v = GObject.Value()
        v.init(GObject.TYPE_UCHAR)
        v.set_uchar(2**8-1)
        v.set_uchar(0)
        self.assertRaises(tests.GIOverflowError, v.set_uchar, 2**8)
        self.assertRaises(tests.GIOverflowError, v.set_uchar, -1)
        v.set_uchar(b"a")
        self.assertRaises(TypeError, v.set_uchar, "")

    def test_value_pointer(self):
        v = GObject.Value()
        v.init(GObject.TYPE_POINTER)
        self.assertRaises(TypeError, v.set_pointer, None)
        v.set_pointer(0)
        v.set_pointer(0xdeadbeef)
        self.assertEqual(v.get_pointer(), 0xdeadbeef)

    def test_value_uint64(self):
        v = GObject.Value()
        v.init(GObject.TYPE_UINT64)
        v.set_uint64(2**64 - 1)
        v.set_uint64(0)
        v.set_uint64(42.50)
        self.assertEqual(v.get_uint64(), 42)
        self.assertRaises(TypeError, v.set_uint64, "a")
        self.assertRaises(tests.GIOverflowError, v.set_uint64, 2**64)
        self.assertRaises(tests.GIOverflowError, v.set_uint64, -1)

    def test_value_string(self):
        v = GObject.Value()
        v.init(GObject.TYPE_STRING)
        v.set_string("foo1")
        self.assertEqual(v.get_string(), "foo1")
        self.assertEqual(v.dup_string(), "foo1")

    def test_gvalue_return(self):
        f = lambda t: GObject.Value().init(t)

        self.assertEqual(f(GObject.TYPE_STRING), None)
        self.assertEqual(f(GObject.TYPE_UINT64), 0)
        self.assertEqual(f(GObject.TYPE_POINTER), None)
        self.assertEqual(f(GObject.TYPE_BOOLEAN), False)

        self.assertEqual(f(GObject.TYPE_DOUBLE), 0)
        self.assertEqual(f(GObject.TYPE_FLOAT), 0)
        self.assertEqual(f(GObject.TYPE_INT), 0)
        self.assertEqual(f(GObject.TYPE_INT64), 0)
        self.assertEqual(f(GObject.TYPE_LONG), 0)
        self.assertEqual(f(GObject.TYPE_OBJECT), None)
        self.assertEqual(f(GObject.TYPE_CHAR), '\x00')
        self.assertEqual(f(GObject.TYPE_UCHAR), b'\x00')
        self.assertEqual(f(GObject.TYPE_UINT), 0)
        self.assertEqual(f(GObject.TYPE_ULONG), 0)

    @skipUnlessGIVersion(3, 4)
    def gvalue_return_gtype(self):
        f = lambda t: GObject.Value().init(t)

        self.assertEqual(f(GObject.TYPE_GTYPE), GObject.TYPE_INVALID)

    def test_float_misc(self):
        Gtk.Button().set_alignment(0.2, 0.4)

    def test_string_none(self):
        entry = Gtk.Entry()
        entry.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY, None)

    def test_flags_in(self):
        spinner = Gtk.Spinner()
        table = Gtk.Table(3, 2, True)
        self.assertRaises(TypeError, table.attach, spinner, 0, 2, 2, 3,
                          xoptions=True)
        self.assertRaises(TypeError, table.attach, spinner, 0, 2, 2, 3,
                          xoptions=-1)
        table.attach(spinner, 0, 2, 2, 3, xoptions=Gtk.AttachOptions.EXPAND)
        table.remove(spinner)
        table.attach(spinner, 0, 2, 2, 3, xoptions=Gtk.AttachOptions.SHRINK)
        table.remove(spinner)
        table.attach(spinner, 0, 2, 2, 3, xoptions=Gtk.AttachOptions.FILL)
        table.remove(spinner)

    def test_filename(self):
        icon = Gtk.IconSource.new()
        icon.set_filename("/tmp/foobar")
        self.assertEqual(icon.get_filename(), "/tmp/foobar")
