# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pgi import _compat

from tests import FIXME


class SignalTest(unittest.TestCase):

    def test_connect(self):
        w = Gtk.Window()
        id_ = w.connect("map", lambda *x: None)
        self.assertTrue(isinstance(id_, _compat.integer_types))
        w.disconnect(id_)

    def test_connect_after(self):
        w = Gtk.Window()
        id_ = w.connect_after("map", lambda *x: None)
        self.assertTrue(isinstance(id_, _compat.integer_types))
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

    def test_connect_user_data(self):
        w = Gtk.Window()
        id_ = w.connect("map", lambda *x: None, 1, 2, 3, 4)
        w.disconnect(id_)

    def test_subclass_connect(self):
        class A(Gtk.Window):
            def __init__(self):
                Gtk.Window.__init__(self)

        class B(A):
            def __init__(self):
                A.__init__(self)

        x = B()
        id_ = x.connect("map", lambda *x: None)
        x.disconnect(id_)

    def test_name_under(self):
        w = Gtk.Window()
        for name in ["scroll-event", "scroll_event"]:
            id_ = w.connect("scroll_event", lambda *x: None)
            self.failUnless(id_ is not None)


class SignalReturnTest(unittest.TestCase):

    @FIXME("some rare random fails..")
    def test_bool(self):
        window = Gtk.OffscreenWindow()
        area = Gtk.DrawingArea()
        window.add(area)
        called = [0]

        def foo(area, context):
            called[0] += 1
            return True
        area.connect("draw", foo)
        area.connect("draw", foo)
        window.show_all()
        for x in xrange(100):
            Gtk.main_iteration_do(False)
        window.destroy()
        self.assertEqual(called[0], 1)
