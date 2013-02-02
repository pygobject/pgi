# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import unittest

from tests import is_gi
from gi.repository import Gtk


class FlagsTest(unittest.TestCase):
    def test_flags(self):
        self.assertEqual(Gtk.RcFlags(1 | 1 << 10), 1 | 1 << 10)
        self.assertEqual(Gtk.RcFlags(1), Gtk.RcFlags.FG)
        self.assertEqual(Gtk.RcFlags(1 | 1 << 3),
                         Gtk.RcFlags.BASE | Gtk.RcFlags.FG)

    def test_or(self):
        x =  Gtk.RcFlags.BASE | Gtk.RcFlags.FG
        self.assertTrue(isinstance(x, Gtk.RcFlags))
        self.assertEqual(int(Gtk.RcFlags.BASE) | int(Gtk.RcFlags.FG), int(x))

    def test_and(self):
        x =  Gtk.RcFlags.BASE & Gtk.RcFlags.FG
        self.assertTrue(isinstance(x, Gtk.RcFlags))
        self.assertEqual(int(Gtk.RcFlags.BASE) & int(Gtk.RcFlags.FG), int(x))

    def test_repr(self):
        self.assertTrue("FG" in repr(Gtk.RcFlags.FG))
        self.assertTrue("0" in repr(Gtk.RcFlags(0)))
        self.assertTrue("GtkRcFlags" in repr(Gtk.RcFlags.BASE))

    @unittest.skipIf(is_gi, "")
    def test_repr_2(self):
        self.assertTrue("NONE" in repr(Gtk.JunctionSides.NONE))

    def test_inval(self):
        self.assertRaises(TypeError, Gtk.RcFlags, "")
        self.assertRaises(TypeError, Gtk.RcFlags, [])
        self.assertRaises(TypeError, Gtk.RcFlags, None)
        self.assertRaises(TypeError, Gtk.RcFlags, 1.1)
        self.assertRaises(OverflowError, Gtk.RcFlags, sys.maxsize + 1)
