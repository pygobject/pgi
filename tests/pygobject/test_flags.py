# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest

from gi.repository import Gtk


class FlagsTest(unittest.TestCase):
    def test_flags(self):
        self.assertEqual(Gtk.RcFlags(1 | 1 << 10), 1 | 1 << 10)
        self.assertEqual(Gtk.RcFlags(1), Gtk.RcFlags.FG)
        self.assertEqual(Gtk.RcFlags(1 | 1 << 3),
                         Gtk.RcFlags.BASE | Gtk.RcFlags.FG)

    def test_repr(self):
        self.assertTrue("FG" in repr(Gtk.RcFlags.FG))
        self.assertTrue("0" in repr(Gtk.RcFlags(0)))
        self.assertTrue("GtkRcFlags" in repr(Gtk.RcFlags.BASE))

    def test_inval(self):
        self.assertRaises(TypeError, Gtk.RcFlags, "")
        self.assertRaises(TypeError, Gtk.RcFlags, [])
        self.assertRaises(TypeError, Gtk.RcFlags, None)
        self.assertRaises(TypeError, Gtk.RcFlags, 1.1)
