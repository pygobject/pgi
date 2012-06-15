# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest
import sys

class MiscTest(unittest.TestCase):
    def test_module_dir(self):
        # make sure all descriptors show up in dir(module)
        self.assertTrue(len(dir(Gtk)) > 1000)

        self.assertEqual(sys.getdefaultencoding(), "ascii")
