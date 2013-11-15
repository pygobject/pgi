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
from gi.repository import GObject, Gtk


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

    @skipIfGI("no basic pytype in gi.. ask for it?")
    def test_pytype(self):
        self.assertTrue(GObject.type_from_name("gint").pytype is int)

    def test_init_(self):
        window_type = Gtk.Window.__gtype__
        self.assertEqual(GObject.GType(Gtk.Window), window_type)
        self.assertEqual(GObject.GType(window_type), window_type)
        self.assertEqual(GObject.GType(window_type), window_type)
