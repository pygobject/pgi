# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest


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
        # FIXME:
        #self.assertEqual(param.value_type, None)

    def test_gtype(self):
        w = Gtk.Window
        self.assertEqual(w.props.transient_for.__gtype__.name, "GParamObject")

    def test_props(self):
        w = Gtk.Window()
        self.assertEqual(w.props.title, None)
