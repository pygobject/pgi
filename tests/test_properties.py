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
        #'flags', 'name', 'nick', 'owner_type', 'value_type'

        # FIXME: pygobject uses the gparamspec flags directly
        self.assertEqual(param.flags & 0xF, 7)
        self.assertEqual(param.name, "transient-for")

    def test_gtype(self):
        w = Gtk.Window
        self.assertEqual(w.props.transient_for.__gtype__.name, "GParamObject")
