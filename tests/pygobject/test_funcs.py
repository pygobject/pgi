# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gtk, GLib


class FuncsTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(Gtk.rc_get_theme_dir(), '/usr/share/themes')
        self.assertTrue(Gtk.rc_get_module_dir().startswith("/"))
        self.assertEqual(Gtk.rc_get_default_files(), [])
        self.assertEqual(Gtk.get_current_event_time(), 0)

    def test_basic_argument(self):
        self.assertEqual(GLib.basename("/omg/foo/test"), "test")
        self.assertEqual(GLib.basename(u"/omg/foo/test"), "test")

    def test_return_guint(self):
        self.assertTrue(isinstance(Gtk.get_binary_age(), (long, int)))

    def test_return_misc(self):
        self.assertTrue(
            isinstance(Gtk.icon_size_register("foo", 1, 2), (int, long)))
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
        self.assertRaises(RuntimeError, builder.add_from_file, "")

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
        a.set_padding(1, 2, 3, 4L)
        a.set_padding(1, 2, 3, 1.9)
        self.assertEqual(a.get_padding(), (1, 2, 3, 1))
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, "")
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, "1")
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, [])
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, None)
        self.assertRaises(ValueError, a.set_padding, 1, 2, 3, -1)
        self.assertRaises(TypeError, a.set_padding, 1, 2, 3, 2+1j)
        self.assertRaises(ValueError, a.set_padding, 1, 2, 3, 2**32)
