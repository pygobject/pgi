# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import unittest

from tests import skipIfGI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


class EnumTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Gtk.WindowPosition.NONE, 0)
        self.assertEqual(Gtk.WindowPosition(1), Gtk.WindowPosition.CENTER)
        self.assertEqual(Gtk.WindowPosition(Gtk.WindowPosition.MOUSE),
                         Gtk.WindowPosition.MOUSE)
        self.assertEqual(Gtk.WindowPosition(Gtk.WindowPosition.MOUSE + 1),
                         Gtk.WindowPosition.CENTER_ALWAYS)

    def test_repr(self):
        self.assertTrue("CENTER" in repr(Gtk.WindowPosition.CENTER))
        self.assertTrue("WindowPosition" in repr(Gtk.WindowPosition(0)))

    def test_inval_value(self):
        self.assertRaises(ValueError, Gtk.WindowPosition, 9)
        self.assertRaises(OverflowError, Gtk.WindowPosition, sys.maxsize + 1)
        self.assertRaises(TypeError, Gtk.WindowPosition, "a")
        self.assertRaises(TypeError, Gtk.WindowPosition, [])
        self.assertRaises(TypeError, Gtk.WindowPosition, 3.0)

    @skipIfGI("no enum methods in gi")
    def test_methods(self):
        self.assertTrue("from_name" in dir(Gtk.IconSize))
        self.assertEqual(Gtk.IconSize.from_name("gtk-menu"), 1)
        self.assertEqual(Gtk.IconSize.get_name(2), "gtk-small-toolbar")
        self.assertEqual(Gtk.IconSize.lookup(1), (True, 16, 16))

    def test_return_enum(self):
        box = Gtk.HBox()
        self.assertEqual(box.get_resize_mode(), Gtk.ResizeMode.PARENT)

    def test_enum_gtype(self):
        self.assertEqual(GObject.GEnum.__gtype__,
                         GObject.GType.from_name("GEnum"))

    @skipIfGI("doesn't work in gi")
    def test_enum_gtype2(self):
        self.assertEqual(Gtk.IconSize.__gtype__.parent.pytype, GObject.GEnum)
