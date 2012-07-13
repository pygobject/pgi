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

    def test_refcount(self):
        w = Gtk.Window()
        self.assertEqual(w.__grefcount__, 2)
        w.destroy()
        self.assertEqual(w.__grefcount__, 1)

    def test_props_construct(self):
        w = Gtk.Window(type=1)
        self.assertEqual(w.props.type, Gtk.WindowType.POPUP)

        w = Gtk.Window()
        self.assertEqual(w.props.type, Gtk.WindowType.TOPLEVEL)


class GTypeTest(unittest.TestCase):
    def test_repr(self):
        a = GObject.GObject()
        t = a.__gtype__
        self.assertTrue("GType" in repr(t))
        self.assertTrue("80" in repr(t))
        self.assertTrue("GObject" in repr(t))

    def test_inval(self):
        a = GObject.GObject()
        t = a.__gtype__
        inval = t.parent
        self.assertEqual(inval, inval.parent)
        self.assertEqual(inval.name, "invalid")
        self.assertTrue("invalid" in repr(inval))
        # pygobject doesn't like it
        #self.assertEqual(inval.pytype, None)

    def test_from_name(self):
        GType = type(GObject.GObject.__gtype__)
        self.assertRaises(RuntimeError, GType.from_name, "foobar")
        wt = Gtk.Widget.__gtype__
        self.assertEqual(wt, GType.from_name("GtkWidget"))

    def test_methods(self):
        wt = Gtk.Widget.__gtype__
        t = GObject.GObject.__gtype__

        self.assertTrue(wt.is_value_type())
        self.assertTrue(t.is_value_type())
        self.assertFalse(wt.is_value_abstract())
        self.assertTrue(t.has_value_table())
        self.assertTrue(wt.is_a(t))
        self.assertFalse(t.is_a(wt))

        self.assertTrue(wt.is_abstract())
        self.assertTrue(wt.is_classed())
        self.assertTrue(wt.is_deep_derivable())
        self.assertTrue(wt.is_derivable())
        self.assertTrue(wt.is_instantiatable())
        self.assertFalse(t.is_abstract())

        self.assertFalse(wt.is_interface())
        self.assertFalse(t.is_interface())

    def test_properties(self):
        wt = Gtk.Widget.__gtype__
        t = GObject.GObject.__gtype__
        self.assertEqual(t.name, "GObject")
        self.assertEqual(t.depth, 1)
        self.assertEqual(wt.fundamental, t)
        self.assertEqual(t.fundamental, t)

    def test_check_missing(self):
        t = GObject.GObject.__gtype__
        dfilter = lambda x: not x.startswith("_")
        self.assertEqual(len(filter(dfilter, dir(t))), 18)

    def test_ptype(self):
        wt = Gtk.Widget.__gtype__
        self.assertEqual(wt.parent.parent.pytype, GObject.Object)
        self.assertEqual(wt.pytype, Gtk.Widget)

    def test_lists(self):
        wt = Gtk.Widget.__gtype__
        # FIXME: interfaces returns some inval
        # and there are not enough children
        self.failUnlessEqual(wt.children[0].pytype, Gtk.Container)
        self.failUnlessEqual(wt.interfaces[0].pytype, Atk.ImplementorIface)
