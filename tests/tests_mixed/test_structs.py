# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from tests import FIXME, skipUnlessCairo


class StructTest(unittest.TestCase):

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
