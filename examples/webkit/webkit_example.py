#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
sys.path.insert(0, '../..')
import pgi
pgi.install_as_gi()

from pgi.repository import WebKit, Gtk


class WebWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.set_default_size(800, 600)
        scroll = Gtk.ScrolledWindow()
        self._view = view = WebKit.WebView()
        scroll.add(view)
        self.add(scroll)

    def load_url(self, url):
        self._view.open(url)


if __name__ == "__main__":
    window = WebWindow()
    window.set_title("App")
    window.load_url("http://www.google.com")
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
