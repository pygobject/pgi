# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
import unittest

from gi.repository import Gtk


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
        self.assertTrue("GtkWindowPosition" in repr(Gtk.WindowPosition(0)))

    def test_inval_value(self):
        self.assertRaises(ValueError, Gtk.WindowPosition, 9)
        self.assertRaises(OverflowError, Gtk.WindowPosition, sys.maxsize + 1)
        self.assertRaises(TypeError, Gtk.WindowPosition, "a")
        self.assertRaises(TypeError, Gtk.WindowPosition, [])
        self.assertRaises(TypeError, Gtk.WindowPosition, 3.0)
