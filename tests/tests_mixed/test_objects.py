# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk, Gio

from tests import skipIfGI

try:
    from gi.repository import Clutter
    Clutter
except ImportError:
    Clutter = None
else:
    status, argv = Clutter.init(sys.argv)
    if status == Clutter.InitError.SUCCESS:
        sys.argv = argv
    else:
        Clutter = None


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
        # newer pygobject adds the namespace
        self.assertTrue("<Window" in r or "<Gtk.Window" in r)
        self.assertTrue("GtkWindow" in r)
        self.assertTrue(str(hex(int(id(w)))) in r)

        g = GObject.Object()
        r = repr(g)
        self.assertTrue("GObject" in r)
        self.assertTrue(str(hex(int(id(g)))) in r)

    def test_obj_type_name(self):
        self.assertEqual(GObject.Object.__name__, "Object")

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

    def test_get_property_unknown(self):
        x = Gtk.HBox()
        self.assertRaises(TypeError, x.get_property, "foobar12")

    def test_get_property(self):
        w = Gtk.Window()
        w.props.title = "foobar"
        self.assertEqual(w.get_property("title"), "foobar")

    def test_non_gir_class(self):
        instance = Gio.File.new_for_path('.')
        instance2 = Gio.File.new_for_path('.')
        # make sure the both share the same class
        self.assertEqual(type(instance), type(instance2))

    def test_field(self):
        self.assertTrue(isinstance(Gtk.Style().xthickness, int))

    def test_method_ownership(self):
        s1 = Gdk.Window.show
        s2 = Gtk.Widget.show
        s3 = Gtk.Window.show

        self.assertFalse(issubclass(Gdk.Window, Gtk.Widget))
        self.assertTrue(issubclass(Gtk.Window, Gtk.Widget))

        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertEqual(s2, s3)

        # here we call the subclass first, but we want the method to still
        # end up at the owner
        g1 = Gtk.Range.get_has_tooltip
        g2 = Gtk.Widget.get_has_tooltip
        self.assertTrue(issubclass(Gtk.Range, Gtk.Widget))
        self.assertEqual(g1, g2)


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

    @unittest.skipUnless(Clutter, "no clutter")
    def test_struct(self):
        ok, color = Clutter.Color.from_string("#33FF33")
        self.assertTrue(ok)
        Clutter.Text(font_name="Mono Bold 24px", text="", color=color)

    @skipIfGI
    def test_construct_error_message(self):
        try:
            Gtk.Label(label=object())
        except TypeError as e:
            self.assertTrue("Gtk.Label" in str(e))
            self.assertTrue("label" in str(e))
