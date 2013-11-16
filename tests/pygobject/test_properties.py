# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version(b"Gtk", b"3.0")
from gi.repository import Gtk, Gdk
from pgi import _compat


class PropertiesTest(unittest.TestCase):
    def test_basic(self):
        w = Gtk.Window
        self.assertTrue(hasattr(w, "props"))
        self.assertTrue(hasattr(w.props, "transient_for"))

    def test_gparam_repr(self):
        w = Gtk.Window
        repr_str = repr(w.props.transient_for)
        self.assertTrue("GParamObject" in repr_str)
        self.assertTrue("'transient-for'" in repr_str)

    def test_gparam(self):
        param = Gtk.Window.props.transient_for

        self.assertEqual(param.flags & 0xF, 7)
        self.assertEqual(param.flags, 231)
        self.assertEqual(param.name, "transient-for")
        self.assertEqual(param.nick, "Transient for Window")
        self.assertEqual(param.owner_type, Gtk.Window.__gtype__)
        self.assertEqual(param.value_type, Gtk.Window.__gtype__)

    def test_gtype(self):
        w = Gtk.Window
        self.assertEqual(w.props.transient_for.__gtype__.name, "GParamObject")

    def test_props(self):
        w = Gtk.Window()
        self.assertEqual(w.props.title, None)
        self.assertTrue(hasattr(w.props, "double_buffered"))
        if _compat.PY2:
            # https://bugzilla.gnome.org/show_bug.cgi?id=705754
            props = [p for p in dir(w.props) if not p.startswith("_")]
            self.assertTrue(len(props) >= 70)

        w = Gtk.Window
        specs = [p for p in dir(w.props) if not p.startswith("_")]
        if _compat.PY2:
            self.assertTrue(len(specs) >= 70)
        self.assertEqual(w.props.double_buffered.name, "double-buffered")

    def test_set_basic(self):
        w = Gtk.Window()
        w.props.title = "foobar"
        self.assertEqual(w.props.title, "foobar")
        w.props.width_request = 42
        self.assertEqual(w.props.width_request, 42)
        w.props.no_show_all = 42
        self.assertEqual(w.props.no_show_all, True)
        w.props.no_show_all = False
        self.assertEqual(w.props.no_show_all, False)

    def test_unicode(self):
        w = Gtk.Window()
        orig = u'\xf6\xe4\xfc'
        w.props.title = u'\xf6\xe4\xfc'
        if _compat.PY2:
            self.assertEqual(w.props.title, orig.encode("utf-8"))
        else:
            self.assertEqual(w.props.title, orig)

    def test_instance(self):
        w = Gtk.Window()
        w.props.title = "a"
        w2 = Gtk.Window()
        w2.props.title = "b"
        self.assertEqual(w.props.title, "a")

    def test_interface_props(self):
        b = Gtk.Box()
        self.assertEqual(b.props.orientation, Gtk.Orientation.HORIZONTAL)
        b.props.orientation = Gtk.Orientation.VERTICAL
        self.assertEqual(b.props.orientation, Gtk.Orientation.VERTICAL)

    def test_invalid(self):
        self.assertRaises(TypeError, Gtk.Box, foo=3)
        self.assertRaises(TypeError, Gtk.Box, 1, "")

    def test_naming(self):
        self.assertTrue("GProps" in repr(Gtk.Box().props))
        self.assertTrue("GProps" in repr(Gtk.Box.props))
        self.assertTrue("GProps" in repr(type(Gtk.Box().props)))
        self.assertTrue("GProps" in repr(type(Gtk.Box.props)))
        self.assertTrue("GParamSpec" in repr(type(Gtk.Box.props.name)))
        self.assertTrue("GParamString" in repr(Gtk.Box.props.name))

    def test_float(self):
        a = Gtk.Alignment()
        a.props.xalign = 0.25
        self.assertEqual(a.props.xalign, 0.25)
        a.props.xalign = 0.5
        self.assertEqual(a.props.xalign, 0.5)

    def test_get_property_uninit(self):
        class Foobar(Gtk.Window):
            def __init__(s):
                self.assertRaises(TypeError, s.get_property, "type")
                Gtk.Window.__init__(s)
        Foobar()

    def test_get_property(self):
        a = Gtk.Alignment()
        a.props.xalign = 0.25
        self.assertEqual(a.get_property("xalign"), 0.25)

        self.assertRaises(TypeError, a.get_property, "foobar")

    def test_get_object(self):
        w = Gtk.Window()
        self.assertTrue(w.get_property("window") is None)
        w.show()
        w.hide()
        window = w.get_property("window")
        self.assertTrue(isinstance(window, Gdk.Window))
