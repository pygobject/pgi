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


class ConstTest(unittest.TestCase):
    def test_int(self):
        self.assertEqual(Gtk.MAJOR_VERSION, 3)
        self.assertEqual(Gtk.PRIORITY_RESIZE, 10)
        self.assertEqual(Gtk.INPUT_ERROR, -1)

    def test_string(self):
        self.assertEqual(Gtk.STYLE_CLASS_SCALE, 'scale')
        self.assertEqual(Gtk.PRINT_SETTINGS_PRINTER, 'printer')
        self.assertEqual(Gtk.STOCK_ABOUT, 'gtk-about')
