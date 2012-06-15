# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest


def test(gi):
    is_pypy = "PyPy" in sys.copyright

    print "#"*80
    if gi:
        if not is_pypy:
            from gi.repository import Gtk
            from gi.repository import GObject
        print "GI"
    else:
        from pgi import Gtk
        from pgi import GObject, GLib
        print "PGI"
    print "#"*80

    if gi and is_pypy:
        print "skipping, no GI with PyPy..."
        return 0

    import __builtin__
    __builtin__.__dict__["Gtk"] = Gtk
    __builtin__.__dict__["GObject"] = GObject

    loader = unittest.defaultTestLoader
    current_dir = os.path.join(os.path.dirname(__file__))
    base_dir = os.path.split(current_dir)[0]
    sys.path.append(base_dir)
    suite = loader.discover(current_dir)
    run = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(run.failures) + len(run.errors)
