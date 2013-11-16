# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import GLib, GObject


class GLibOverrrideTest(unittest.TestCase):
    def test_idle_add(self):
        GObject.idle_add is GLib.idle_add
        GLib.idle_add(lambda *x: None)
        GLib.idle_add(lambda *x: None, priority=GLib.PRIORITY_DEFAULT_IDLE)

    def test_source_remove(self):
        GObject.source_remove is GLib.source_remove
