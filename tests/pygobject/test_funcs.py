# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest

from gi.repository import Gtk, GLib


class FuncsTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(Gtk.rc_get_theme_dir(), '/usr/share/themes')
        self.assertTrue(Gtk.rc_get_module_dir().startswith("/"))
        self.assertEqual(Gtk.rc_get_default_files(), [])
        self.assertEqual(Gtk.get_current_event_time(), 0)

    def test_basic_argument(self):
        self.assertEqual(GLib.basename("/omg/foo/test"), "test")
        self.assertEqual(GLib.basename(u"/omg/foo/test"), "test")
