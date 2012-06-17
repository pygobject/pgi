# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi import Gtk
from _override import override


Gtk.init()

class Window(Gtk.Window):
    def __init__(self, title):
        super(Window, self).__init__()
        self.set_title(title)

override(Window)
