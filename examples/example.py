# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
sys.path.insert(0, '..')
import pgi
pgi.replace_gi()

from gi.repository import Gtk


if __name__ == '__main__':
    b = Gtk.Window(title="Helllloooo")
    b.show_all()
    b.connect("destroy", lambda *x: Gtk.main_quit())
    Gtk.main()
