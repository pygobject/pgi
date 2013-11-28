# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class InterfaceTest(unittest.TestCase):
    def test_iface(self):
        #self.assertRaises(NotImplementedError, Gtk.Editable)
        self.assertTrue("delete_text" in dir(Gtk.Editable))

    def test_obj_iface(self):
        self.assertTrue(Gtk.Buildable in Gtk.Bin.__mro__)
        self.assertTrue(Gtk.Buildable not in Gtk.Bin.__bases__)
