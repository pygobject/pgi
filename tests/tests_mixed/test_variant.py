# Copyright 2016 Linus Lewandowski
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import GLib

class VariantTest(unittest.TestCase):

    def test_variant(self):
        s1 = GLib.Variant("s", "aaa")
        s2 = GLib.Variant.new_string("aaa")
        v1 = GLib.Variant("v", s1)
        v2 = GLib.Variant.new_variant(s2)
        a = GLib.Variant("as", ["aaa"])

        variants = [s1, s2, v1, v2, a]
        for v in variants:
            assert(isinstance(v, GLib.Variant))

        assert(str(s1) == "'aaa'")
        assert(str(s2) == "'aaa'")
        assert(str(v1) == "<'aaa'>")
        assert(str(v2) == "<'aaa'>")
        assert(str(a)  == "['aaa']")

        assert(repr(s1) == "GLib.Variant('s', 'aaa')")
        assert(repr(s2) == "GLib.Variant('s', 'aaa')")
        assert(repr(v1) == "GLib.Variant('v', <'aaa'>)")
        assert(repr(v2) == "GLib.Variant('v', <'aaa'>)")
        assert(repr(a)  == "GLib.Variant('as', ['aaa'])")

        assert(s1.unpack() == "aaa")
        assert(s2.unpack() == "aaa")
        assert(v1.unpack() == "aaa")
        assert(v2.unpack() == "aaa")
        assert(a.unpack() == ["aaa"])
