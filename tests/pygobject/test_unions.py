# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gdk, Gtk, GObject


class UnionTest(unittest.TestCase):
    def test_union(self):
        e = Gdk.Event()
        repr(e)

    def test_class(self):
        c = GLib.DoubleIEEE754
        self.assertTrue("GLib" in c.__module__)
        self.assertTrue("DoubleIEEE754" in c.__name__)

    def test_fields(self):
        self.assertTrue("type" in dir(Gdk.Event))
        a = Gdk.Event.new(Gdk.EventType.PROXIMITY_IN)
        self.assertEqual(a.type, Gdk.EventType.PROXIMITY_IN)

    def test_methods(self):
        self.assertTrue("new" in dir(Gdk.Event))
        e = Gdk.Event()
        n = Gdk.Event.new(Gdk.EventType.DELETE)
        self.assertTrue(type(e) is type(n))

    def test_structs(self):
        a = Gtk.BindingArg()
        g = a.arg_type
        self.assertEqual(g, GObject.TYPE_INVALID)

    def test_uint16_field(self):
        color = Gdk.Color(1, 2, 3)
        self.assertEqual(color.red, 1)
        self.assertEqual(color.green, 2)
        self.assertEqual(color.blue, 3)

    def test_uint32_field(self):
        color = Gdk.Color(1, 2, 3)
        color.pixel = 42
        self.assertEqual(color.pixel, 42)
