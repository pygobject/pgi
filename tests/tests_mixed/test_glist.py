# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

import tests

from gi.repository import GObject

try:
    from gi.repository import GIMarshallingTests
    GIMarshallingTests
except ImportError:
    GIMarshallingTests = None


def skipUnlessGIMarshallingTests(func):
    return unittest.skipUnless(GIMarshallingTests,
                               "GIMarshallingTests missing")(func)


@skipUnlessGIMarshallingTests
class GListTest(unittest.TestCase):

    def test_corner_cases(self):
        self.assertRaises(
            TypeError, GIMarshallingTests.glist_int_none_in, [object()])

        self.assertRaises(tests.GIOverflowError,
            GIMarshallingTests.glist_int_none_in, [GObject.G_MAXUINT64])

        class SomeInt(object):
            def __init__(self, val):
                self.val = val

            def __int__(self):
                return self.val

        GIMarshallingTests.glist_int_none_in([SomeInt(-1), 0, 1, 2])
