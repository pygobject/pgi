# -*- coding: utf-8 -*-
# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import time


def run(load_gi):
    if not load_gi:
        import pgi
        pgi.replace_gi()

    import gi

    if load_gi:
        assert gi.__name__ == "gi"
        print "### GI " + "#" * 61
    else:
        assert gi.__name__ == "pgi"
        print "### PGI " + "#" * 60

    t = time.time()
    from gi.repository import Gtk, GObject, GLib, Gio, Pango, Gdk
    t = time.time() - t
    print "%15s: %5.2f ms" % ("import", t * (10 ** 3))

    def bench_constants(n):
        for i in xrange(n):
            Gtk.MAJOR_VERSION

    def bench_flags(n):
        for i in xrange(n):
            Gtk.RcFlags(1 | 1 << 10)
            Gtk.RcFlags.TEXT - 1
            Gtk.RcFlags.BASE | Gtk.RcFlags.FG

    def bench_func(n):
        for i in xrange(n):
            Gtk.get_current_event_time()
            Gtk.rc_get_theme_dir()[:]

    def bench_gtype(n):
        for i in xrange(n):
            GObject.Object.__gtype__.children
            GObject.Object.__gtype__.pytype

    def bench_object(n):
        for i in xrange(n):
            w = Gtk.Window()
            w.props.title = "this"

    def bench_method(n):
        for i in xrange(n):
            b = Gtk.Button()
            b.set_name("foobar")

    bench = [
        (bench_constants, 100000),
        (bench_flags, 100000),
        (bench_func, 100000),
        (bench_method, 1000),
        (bench_gtype, 100000),
        (bench_object, 10000),
    ]

    for b, n in bench:
        t = time.time()
        b(n)
        t = time.time() - t
        print "%15s: %5.2f µs" % (b.__name__, t * (10 ** 6) / float(n))
