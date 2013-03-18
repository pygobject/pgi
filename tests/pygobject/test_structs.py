# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gtk

from tests import is_gi


class StructTest(unittest.TestCase):

    @unittest.skipUnless(is_gi, "FIXME")
    def test_foreign_cairo(self):
        window = Gtk.OffscreenWindow()
        area = Gtk.DrawingArea()
        window.add(area)

        def foo(area, context):
            self.assertTrue(hasattr(context, "set_source_rgb"))
        area.connect("draw", foo)

        window.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()
        window.destroy()
