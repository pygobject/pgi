#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2011 Sebastian Pölsterl
#
# Permission is granted to copy, distribute and/or modify this document
# under the terms of the GNU Free Documentation License, Version 1.3
# or any later version published by the Free Software Foundation;
# with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.

import sys
sys.path.insert(0, '../..')
import pgi
pgi.install_as_gi()

from gi.repository import Gtk

class ButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Button Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button(stock=Gtk.STOCK_OPEN)
        button.connect("clicked", self.on_open_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("_Close", use_underline=True)
        button.connect("clicked", self.on_close_clicked)
        hbox.pack_start(button, True, True, 0)

    def on_click_me_clicked(self, button):
        print "\"Click me\" button was clicked"

    def on_open_clicked(self, button):
        print "\"Open\" button was clicked"

    def on_close_clicked(self, button):
        print "Closing application"
        Gtk.main_quit()

win = ButtonWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
