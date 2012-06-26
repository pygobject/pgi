# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
sys.path.insert(0, '..')

from pgi.repository import Gtk


if __name__ == '__main__':
    b = Gtk.Window("Helllloooo")
    b.show_all()
    Gtk.main()
