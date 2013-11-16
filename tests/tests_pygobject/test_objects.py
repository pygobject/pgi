# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Atk, Gdk, Gio

try:
    from gi.repository import Clutter
except ImportError:
    Clutter = None

from tests import skipIfGI, FIXME


class ObjectTest(unittest.TestCase):

    def test_classes(self):
        g = GObject.Object()
        self.assertTrue(isinstance(g, GObject.Object))
        a = Gtk.AccelMap()
        self.assertTrue(isinstance(a, type(g)))

    def test_init_1(self):
        class A(GObject.Object):
            def __init__(self, foo):
                GObject.Object.__init__(self)
                self.foo = foo

        class B(A):
            def __init__(self, x):
                A.__init__(self, x)

        self.assertEqual(B(3).foo, 3)

    def test_init_2(self):
        class B(object):
            pass

        class A(B, GObject.Object):
            def __init__(self):
                GObject.Object.__init__(self)
                B.__init__(self)

        A()

    def test_gtk(self):
        w = Gtk.Window()
        w.set_title("foobar")
        self.assertEqual(w.get_title(), "foobar")

    def test_obj_repr(self):
        w = Gtk.Window()
        r = repr(w)
        self.assertTrue("<Window" in r)
        self.assertTrue("GtkWindow" in r)
        self.assertTrue(str(hex(int(id(w)))) in r)

        g = GObject.Object()
        r = repr(g)
        self.assertTrue("GObject" in r)
        self.assertTrue(str(hex(int(id(g)))) in r)

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
        self.assertEqual(table.__grefcount__, 1)
        self.assertTrue(table)
        table.destroy()

        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.assertTrue(isinstance(cb, Gtk.Clipboard))

        Gtk.Adjustment(0, 0, 100, 1, 10, 0)

    def test_init_propagate(self):
        b = Gtk.CheckButton("foo")
        self.assertEqual(b.get_label(), "foo")

    def test_refs(self):
        button = Gtk.Button.new()
        self.assertEqual(button.__grefcount__, 1)
        button = Gtk.Button()
        self.assertEqual(button.__grefcount__, 1)
        box = Gtk.HBox()
        box.add(button)
        self.assertEqual(button.__grefcount__, 2)
        box.remove(button)
        self.assertEqual(button.__grefcount__, 1)
        box.add(button)
        self.assertEqual(button.__grefcount__, 2)
        box.destroy()
        self.assertEqual(button.__grefcount__, 1)

        a = Gio.FilenameCompleter()
        self.assertEqual(a.__grefcount__, 1)

    def test_hashable(self):
        b = Gtk.Button()
        v = GObject.Value()
        v.init(GObject.TYPE_OBJECT)
        v.set_object(b)
        b2 = v.get_object()
        self.assertEqual(b, b2)
        self.assertEqual(len(set([b, b2])), 1)

    def test_create_from_gtype(self):
        out = Gio.File.new_for_path("")
        self.assertTrue("GLocalFile" in repr(out))

    def test_abstract_init(self):
        self.assertRaises(TypeError, Gtk.Widget)

    def test_set_property_unknown(self):
        x = Gtk.HBox()
        self.assertRaises(TypeError, x.set_property, "foobar123", "blah")

    def test_set_property_invalid(self):
        x = Gtk.HBox()
        x.set_property("orientation", Gtk.Orientation.VERTICAL)
        self.assertRaises(TypeError, x.set_property, "orientation", None)

    def test_set_property_enum(self):
        x = Gtk.HBox()
        self.assertEqual(x.props.orientation, Gtk.Orientation.HORIZONTAL)
        x.set_property("orientation", Gtk.Orientation.VERTICAL)
        self.assertEqual(x.props.orientation, Gtk.Orientation.VERTICAL)

    @FIXME
    def test_get_property_unknown(self):
        x = Gtk.HBox()
        self.assertRaises(TypeError, x.get_property, "foobar12")

    @FIXME
    def test_get_property(self):
        w = Gtk.Window()
        w.props.title = "foobar"
        self.assertEqual(w.get_property("title"), "foobar")

    def test_non_gir_class(self):
        instance = Gio.File.new_for_path('.')
        instance2 = Gio.File.new_for_path('.')
        # make sure the both share the same class
        self.assertEqual(type(instance), type(instance2))


class GObjectConstructTest(unittest.TestCase):
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

    def test_props_construct_null(self):
        w = Gtk.ScrolledWindow()
        w.destroy()

    def test_props_construct_inval(self):
        self.assertRaises(TypeError,
                          lambda x: Gtk.ScrolledWindow(**x), dict(foo=3))

    @skipIfGI("no gi clutter overrides")
    @unittest.skipUnless(Clutter, "no clutter")
    def test_struct(self):
        Clutter.Text("Mono Bold 24px", "",
                     Clutter.Color.from_string("#33FF33"))


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
        self.assertEqual(len(list(filter(dfilter, dir(t)))), 18)

    def test_ptype(self):
        wt = Gtk.Widget.__gtype__
        self.assertEqual(wt.parent.parent.pytype, GObject.Object)
        self.assertEqual(wt.pytype, Gtk.Widget)

    def test_lists(self):
        wt = Gtk.Window.__gtype__
        children = set([x.pytype for x in wt.children])
        self.assertTrue(Gtk.Dialog in children)
        interfaces = set([x.pytype for x in wt.interfaces])
        should = set([Atk.ImplementorIface, Gtk.Buildable])
        self.assertEqual(interfaces, should)

    def test_interfaces(self):
        t = Gtk.Editable.__gtype__
        self.assertEqual(t.parent.pytype, None)
        self.assertTrue(t.is_interface)
