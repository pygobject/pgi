# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest
import sys

from gi import get_required_version, require_version
from gi.repository import Gtk, GObject, GLib, Gdk


class MiscTest(unittest.TestCase):
    def test_module_dir(self):
        # make sure all descriptors show up in dir(module)
        self.assertTrue(len(dir(Gtk)) > 1000)

        self.assertEqual(sys.getdefaultencoding(), "ascii")

        self.assertEqual(Gtk._version, "3.0")
        self.assertEqual(GObject._version, "2.0")
        self.assertEqual(GLib._version, "2.0")

    def test_require_version(self):
        self.assertTrue(get_required_version("Gtk") is None)
        self.assertTrue(require_version("Gtk", "3.0") is None)
        self.assertRaises(ValueError, require_version, "Gtk", "4.0")
        self.assertRaises(ValueError, require_version, "Gtk", "2.0")
        self.assertEqual(get_required_version("Gtk"), "3.0")
        self.assertTrue(get_required_version("...") is None)
        self.assertRaises(ValueError, require_version, "...", "3.0")

    def test_import(self):
        self.assertRaises(ImportError, __import__,
                          "gi.repository.FooBar", fromlist=[""])

    def test_module(self):
        self.assertTrue(Gtk.__path__.endswith(".typelib"))
        self.assertTrue(Gtk.__loader__)
        self.assertTrue(Gtk.__file__.endswith(".repository.Gtk>"))

    def test_structure(self):
        a = Gdk.atom_intern('CLIPBOARD', True)
        self.assertTrue(isinstance(a, Gdk.Atom))
        self.assertTrue(isinstance(Gtk.Clipboard.get(a), Gtk.Clipboard))
        self.assertRaises(TypeError, Gtk.Clipboard.get, None)
        self.assertRaises(TypeError, Gtk.Clipboard.get, 0)
        self.assertRaises(TypeError, Gtk.Clipboard.get, Gdk.Atom)
        self.assertRaises(TypeError, Gdk.Atom, "baz")
