# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gtk, GObject, Atk, Gdk


class ObjectTest(unittest.TestCase):

    def test_classes(self):
        g = GObject.Object()
        self.assertTrue(isinstance(g, GObject.Object))
        a = Gtk.AccelMap()
        self.assertTrue(isinstance(a, type(g)))

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

        w = Gtk.Window(title="test123")
        self.assertEqual(w.props.title, "test123")

        w = Gtk.Window(title=u"test123")
        self.assertTrue(isinstance(w.props.title, str))
        self.assertEqual(w.props.title, "test123")

    def test_construcor(self):
        self.assertTrue(Gtk.Label.new("foo"))
        w = Gtk.Label.new_with_mnemonic("foobar")
        self.assertTrue(w)
        self.assertTrue(isinstance(w, Gtk.Widget))
        self.assertTrue(isinstance(w, Gtk.Label))

    def test_misc(self):
        dialog = Gtk.Dialog()
        self.assertTrue(dialog)
        dialog.destroy()

        table = Gtk.Table(3, 2)
        self.assertTrue(table)
        table.destroy()

        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.assertTrue(isinstance(cb, Gtk.Clipboard))

        Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        b = Gtk.CheckButton("foo")
        # FIXME: pass args/kwargs to bases (in this case a override)
        # self.assertEqual(b.get_label(), "foo")


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
        wt = Gtk.Window.__gtype__
        children = set([x.pytype for x in wt.children])
        self.assertEqual(children, set([Gtk.Dialog]))
        interfaces = set([x.pytype for x in wt.interfaces])
        should = set([Atk.ImplementorIface, Gtk.Buildable])
        self.assertEqual(interfaces, should)

    def test_interfaces(self):
        t = Gtk.Editable.__gtype__
        self.assertEqual(t.parent.pytype, None)
        self.assertTrue(t.is_interface)

class SignalTest(unittest.TestCase):

    def test_connect(self):
        w = Gtk.Window()
        id_ = w.connect("map", lambda *x: None)
        self.assertTrue(isinstance(id_, (long, int)))
        w.disconnect(id_)

    def test_connect_after(self):
        w = Gtk.Window()
        id_ = w.connect_after("map", lambda *x: None)
        self.assertTrue(isinstance(id_, (long, int)))
        w.disconnect(id_)

    def test_handler_block(self):
        w = Gtk.Window()
        id_ = w.connect_after("map", lambda *x: None)
        w.handler_block(id_)
        w.handler_unblock(id_)
        w.disconnect(id_)

    def test_connect_invalid(self):
        w = Gtk.Window()
        self.assertRaises(TypeError, w.connect, "map", None)
        self.assertRaises(TypeError, w.connect, "foobar", lambda *x: None)
        self.assertRaises(TypeError, w.connect_after, "foobar", lambda: None)
