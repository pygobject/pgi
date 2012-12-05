# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gtk


class InterfaceTest(unittest.TestCase):
    def test_iface(self):
        #self.assertRaises(NotImplementedError, Gtk.Editable)
        self.assertTrue("delete_text" in dir(Gtk.Editable))

    def test_obj_iface(self):
        #print Gtk.Entry
        pass
