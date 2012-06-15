# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest


class ObjectTest(unittest.TestCase):

    def test_classes(self):
        g = GObject.Object()
        self.assertTrue(isinstance(g, GObject.Object))
        a = Gtk.AccelMap()
        self.assertTrue(isinstance(a, type(g)))

    def test_gobject(self):
        c = Gtk.AccelMap()
        c.set_data("xx", 3)

        g = GObject.Object()
        g.set_data("xx", 42)
        self.assertEqual(g.get_data("xx"), 42)

        a = GObject.Object()
        a.set_data("xx", 24)
        self.assertEqual(a.get_data("xx"), 24)

        self.assertEqual(g.get_data("xx"), 42)
        self.assertEqual(c.get_data("xx"), 3)
