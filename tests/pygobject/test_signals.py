# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gtk, GObject, Atk, Gdk, Gio


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

    def test_connect_user_data(self):
        w = Gtk.Window()
        id_ = w.connect("map", lambda *x: None, 1, 2, 3, 4)
        w.disconnect(id_)
