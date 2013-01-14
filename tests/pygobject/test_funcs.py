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

        b.set_alignment(0.3, 0.4)
