# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gdk


class UnionTest(unittest.TestCase):
    def test_union(self):
        e = Gdk.Event()
        repr(e)

    def test_fields(self):
        self.assertTrue("type" in dir(Gdk.Event))
        a = Gdk.Event.new(Gdk.EventType.PROXIMITY_IN)
        self.assertEqual(a.type, Gdk.EventType.PROXIMITY_IN)

    def test_methods(self):
        self.assertTrue("new" in dir(Gdk.Event))
        e = Gdk.Event()
        n = Gdk.Event.new(Gdk.EventType.DELETE)
        self.assertTrue(type(e) is type(n))
