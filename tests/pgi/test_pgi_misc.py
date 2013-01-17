# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi.util import escape_name, unescape_name


class PGIMisc(unittest.TestCase):
    def test_escape_property(self):
        self.assertEqual(escape_name("class"), "class_")
        self.assertEqual(escape_name("cla-ss"), "cla_ss")

    def test_unescape_property(self):
        self.assertEqual(unescape_name("foo_"), "foo")
        self.assertEqual(unescape_name("fo_oo_"), "fo-oo")
