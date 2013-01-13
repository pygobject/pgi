# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
sys.path.insert(0, '..')
import pgi
pgi.install_as_gi()

from gi.repository import Gtk


if __name__ == '__main__':
    b = Gtk.Window(title="Helllloooo")
    b.show_all()
    b.connect("destroy", lambda *x: Gtk.main_quit())
    Gtk.main()
