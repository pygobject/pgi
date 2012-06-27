# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest


def test(gi):
    print "#" * 80
    if gi:
        from gi.repository import Gtk, GObject, GLib, Atk, Gdk
        print "GI"
    else:
        from pgi.repository import Gtk, GObject, GLib, Atk, Gdk
        print "PGI"
    print "#" * 80

    import __builtin__
    __builtin__.__dict__["Gtk"] = Gtk
    __builtin__.__dict__["GObject"] = GObject
    __builtin__.__dict__["GLib"] = GLib
    __builtin__.__dict__["Atk"] = Atk

    loader = unittest.defaultTestLoader
    current_dir = os.path.join(os.path.dirname(__file__))
    base_dir = os.path.split(current_dir)[0]
    sys.path.append(base_dir)
    suite = loader.discover(current_dir)
    run = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(run.failures) + len(run.errors)
