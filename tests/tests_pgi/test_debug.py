# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi.debug import pprint
from pgi._compat import StringIO
from pgi.repository import Gtk


class TDebug(unittest.TestCase):

    def test_pprint_function(self):
        file_ = StringIO()
        pprint(Gtk.main, file_)
        self.assertTrue("main() -> None" in file_.getvalue())

    def test_pprint_class(self):
        # populate cache
        Gtk.Window()

        file_ = StringIO()
        pprint(Gtk.Window, file_)
        docstring = "Gtk.Window(type: Gtk.WindowType) -> Gtk.Window"
        self.assertTrue(docstring in file_.getvalue())
