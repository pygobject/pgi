# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest


class ObjectTest(unittest.TestCase):

    def test_classes(self):
        g = GObject.Object()
        self.assertTrue(isinstance(g, GObject.Object))
        a = Gtk.AccelMap()
        self.assertTrue(isinstance(a, type(g)))

    def test_gobject(self):
        c = Gtk.AccelMap()
        c.set_data("xx", 3)

        g = GObject.Object()
        g.set_data("xx", 42)
        self.assertEqual(g.get_data("xx"), 42)

        a = GObject.Object()
        a.set_data("xx", 24)
        self.assertEqual(a.get_data("xx"), 24)

        self.assertEqual(g.get_data("xx"), 42)
        self.assertEqual(c.get_data("xx"), 3)

    def test_gtk(self):
        w = Gtk.Window()
        w.set_title("foobar")
        self.assertEqual(w.get_title(), "foobar")

    def test_obj_repr(self):
        w = Gtk.Window()
        r = repr(w)
        self.assertTrue("<Window" in r)
        self.assertTrue("GtkWindow" in r)
        self.assertTrue(str(hex(id(w))) in r)

        g = GObject.Object()
        r = repr(g)
        self.assertTrue("GObject" in r)
        self.assertTrue(str(hex(id(g))) in r)

    def test_mro(self):
        klass = Gtk.Window
        parents = [Gtk.Bin, Gtk.Container, Gtk.Widget, GObject.Object]
        for parent in parents:
            self.assertTrue(parent in klass.__mro__)

    def test_class(self):
        self.assertTrue("Gtk" in Gtk.Window().__module__)
        self.assertEqual(Gtk.Window.__name__, "Window")

    def test_gobject_duplicate(self):
        self.assertEqual(GObject.GObject, GObject.Object)
        self.assertTrue(issubclass(Gtk.Widget, GObject.GObject))
        self.assertTrue(issubclass(Gtk.Widget, GObject.Object))
