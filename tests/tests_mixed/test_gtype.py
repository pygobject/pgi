# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from tests import skipIfGI

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk, Atk


class GTypeTest(unittest.TestCase):
    def test_type_name(self):
        self.assertEqual(GObject.type_name(GObject.TYPE_NONE), 'void')
        self.assertEqual(GObject.type_name(GObject.TYPE_OBJECT), 'GObject')

    def test_from_name(self):
        self.assertEqual(GObject.type_from_name("glong"), GObject.TYPE_LONG)
        self.assertEqual(
            GObject.type_from_name("GObject"), GObject.TYPE_OBJECT)
        # gi fails..
        try:
            self.assertEqual(
                GObject.type_from_name("invalid"), GObject.TYPE_INVALID)
        except RuntimeError:
            pass

        self.assertRaises(TypeError, GObject.GType.from_name, None)
        self.assertRaises(TypeError, GObject.GType.from_name, [])
        GObject.GType.from_name(u"void")

    def test_from_name2(self):
        GType = type(GObject.GObject.__gtype__)
        self.assertRaises(RuntimeError, GType.from_name, "foobar")
        wt = Gtk.Widget.__gtype__
        self.assertEqual(wt, GType.from_name("GtkWidget"))

    @skipIfGI("no basic pytype in gi.. ask for it?")
    def test_pytype(self):
        self.assertTrue(GObject.type_from_name("gint").pytype is int)

    @skipIfGI
    def test_pytype_2(self):
        self.assertTrue(GObject.type_from_name("GStrv").pytype == [str])

    def test_init_(self):
        window_type = Gtk.Window.__gtype__
        self.assertEqual(GObject.GType(Gtk.Window), window_type)
        self.assertEqual(GObject.GType(window_type), window_type)
        self.assertEqual(GObject.GType(window_type), window_type)

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

    @skipIfGI
    def test_inval2(self):
        a = GObject.GObject()
        t = a.__gtype__
        inval = t.parent
        # pygobject doesn't like it
        self.assertEqual(inval.pytype, None)

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
