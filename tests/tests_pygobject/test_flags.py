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
from gi.repository import Gtk, GLib


class FlagsTest(unittest.TestCase):
    def test_flags(self):
        self.assertEqual(Gtk.RcFlags(1 | 1 << 10), 1 | 1 << 10)
        self.assertEqual(Gtk.RcFlags(1), Gtk.RcFlags.FG)
        self.assertEqual(Gtk.RcFlags(1 | 1 << 3),
                         Gtk.RcFlags.BASE | Gtk.RcFlags.FG)

    def test_or(self):
        x = Gtk.RcFlags.BASE | Gtk.RcFlags.FG
        self.assertTrue(isinstance(x, Gtk.RcFlags))
        self.assertEqual(int(Gtk.RcFlags.BASE) | int(Gtk.RcFlags.FG), int(x))

    def test_and(self):
        x = Gtk.RcFlags.BASE & Gtk.RcFlags.FG
        self.assertTrue(isinstance(x, Gtk.RcFlags))
        self.assertEqual(int(Gtk.RcFlags.BASE) & int(Gtk.RcFlags.FG), int(x))

    def test_repr(self):
        self.assertTrue("FG" in repr(Gtk.RcFlags.FG))
        self.assertTrue("0" in repr(Gtk.RcFlags(0)))
        self.assertTrue("RcFlags" in repr(Gtk.RcFlags.BASE))

    @skipIfGI
    def test_repr_2(self):
        self.assertTrue("NONE" in repr(Gtk.JunctionSides.NONE))

    def test_inval(self):
        self.assertRaises(TypeError, Gtk.RcFlags, "")
        self.assertRaises(TypeError, Gtk.RcFlags, [])
        self.assertRaises(TypeError, Gtk.RcFlags, None)
        self.assertRaises(TypeError, Gtk.RcFlags, 1.1)

    @skipIfGI("broken since gi 3.8")
    def test_overflow(self):
        # https://bugzilla.gnome.org/show_bug.cgi?id=698765
        self.assertRaises(OverflowError, Gtk.RcFlags, sys.maxsize + 1)

    def test_no_value_nick(self):
        self.assertEqual(GLib.IOCondition(0).first_value_nick, None)
        self.assertEqual(GLib.IOCondition(0).first_value_name, None)
        self.assertEqual(GLib.IOCondition(0).value_names, [])
        self.assertEqual(GLib.IOCondition(0).value_nicks, [])

    def test_value_nicks_names(self):
        self.assertEqual(GLib.IOCondition(3).value_nicks, ["in", "pri"])
        self.assertEqual(GLib.IOCondition(3).value_names,
                         ["G_IO_IN", "G_IO_PRI"])
        self.assertEqual(GLib.IOCondition(3).first_value_nick, "in")
        self.assertEqual(GLib.IOCondition(3).first_value_name, "G_IO_IN")
