# Copyright 2013, 2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Atk, Gio, GLib

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

from tests import FIXME, skipUnlessCairo, skipIfGI


class StructTest(unittest.TestCase):

    @FIXME
    @skipUnlessCairo
    def test_foreign_cairo(self):
        window = Gtk.OffscreenWindow()
        area = Gtk.DrawingArea()
        window.add(area)

        def foo(area, context):
            self.assertTrue(hasattr(context, "set_source_rgb"))
        area.connect("draw", foo)

        window.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()
        window.destroy()

    def test_struct_out_simple(self):
        button = Gtk.Button()
        req = button.size_request()
        self.assertTrue(req)
        self.assertTrue(isinstance(req.height, int))

    @FIXME
    def test_struct_out_simple_leak(self):
        button = Gtk.Button()
        req = button.size_request()
        self.assertTrue(req._needs_free)

    def test_struct_out(self):
        model = Gtk.ListStore(int)
        iter_ = model.insert_with_valuesv(0, [], [])
        self.failUnless(isinstance(iter_, Gtk.TreeIter))

    def test_struct_copy(self):
        iter_ = Gtk.TreeIter()
        iter_.stamp = 4
        new = iter_.copy()
        self.failUnlessEqual(new.stamp, 4)
        iter_.stamp = 999
        self.failUnlessEqual(new.stamp, 4)
        self.failUnlessEqual(iter_.stamp, 999)

    @FIXME
    def test_foo(self):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.state

    @skipIfGI
    def test_field_info(self):
        self.assertEqual(Gdk.Color.pixel.py_type, int)
        self.assertEqual(Gdk.Color.pixel.name, "pixel")
        self.assertTrue(Gdk.Color.pixel.writeable)
        self.assertTrue(Gdk.Color.pixel.readable)

        self.assertEqual(Gdk.EventButton.device.py_type, Gdk.Device)

    def test_utf8_field(self):
        a = Atk.Object()
        a.set_name("foo")
        self.assertEqual(a.name, "foo")

    @skipIfGI
    @unittest.skipUnless(Clutter, "no clutter")
    def test_unichar_field(self):
        field = Clutter.KeyEvent.unicode_value
        self.assertTrue(field.py_type is str)
        self.assertEqual(field.name, "unicode_value")

    @skipIfGI
    def test_error_field(self):
        try:
            gi.require_version('EvinceView', '3.0')
            from gi.repository import EvinceView
        except (ImportError, ValueError):
            return

        field = EvinceView.JobFonts.error
        self.assertTrue(field.py_type is GLib.GError)
        self.assertEqual(field.name, "error")

    def test_boolean_field(self):
        a = Gtk.RecentData()
        self.assertTrue(isinstance(a.is_private, bool))

        for is_true in [True, 42, -1]:
            a.is_private = is_true
            self.assertTrue(a.is_private)

        # FIXME: None should also work
        for is_false in [False, 0]:
            a.is_private = is_false
            self.assertFalse(a.is_private)

    def test_allow_none_in(self):
        self.assertTrue(Gio.SimpleAction.new("foo", None))
