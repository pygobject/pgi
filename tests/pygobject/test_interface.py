# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest

from gi.repository import Gtk


class InterfaceTest(unittest.TestCase):
    def test_iface(self):
        #self.assertRaises(NotImplementedError, Gtk.Editable)
        self.assertTrue("delete_text" in dir(Gtk.Editable))

    def test_obj_iface(self):
        #print Gtk.Entry
        pass
