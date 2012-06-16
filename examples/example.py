# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
sys.path.append('..')

from pgi import Gtk


if __name__ == '__main__':
    Gtk.init()
    b = Gtk.Window()
    b.show_all()
    Gtk.main()
