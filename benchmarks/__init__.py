# -*- coding: utf-8 -*-
# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import time


def run(load_gi, backend=None):
    if not load_gi:
        import pgi
        pgi.install_as_gi()
        try:
            pgi.set_backend(backend)
        except LookupError:
            print("Couldn't load backend: %r" % backend)
            return

    import gi

    if load_gi:
        assert gi.__name__ == "gi"
        hl = "### GI " + "#" * 100
    else:
        assert gi.__name__ == "pgi"
        if backend:
            hl = "### PGI (%s) " % backend + "#" * 100
        else:
            hl = "### PGI " + "#" * 100
    print(hl[:80])

    t = time.time()
    from gi.repository import Gtk, GObject, GLib, Gio, Pango, Gdk
    GLib = GLib
    Gio = Gio
    Pango = Pango
    Gdk = Gdk
    t = time.time() - t
    print("%15s: %5.2f ms" % ("import", t * (10 ** 3)))

    def bench_flags(n):
        times = []
        for i in xrange(n):
            t = time.time()
            Gtk.RcFlags(1 | 1 << 10)
            Gtk.RcFlags.TEXT - 1
            Gtk.RcFlags.BASE | Gtk.RcFlags.FG
            t = time.time() - t
            times.append(t)
        return times

    def bench_func(n):
        times = []
        for i in xrange(n):
            t = time.time()
            Gtk.get_current_event_time()
            Gtk.rc_get_theme_dir()[:]
            t = time.time() - t
            times.append(t)
        return times

    def bench_gvalue(n):
        times = []
        b = Gtk.Button()
        for i in xrange(n):
            t = time.time()
            value = GObject.Value()
            value.init(GObject.TYPE_INT)
            value.set_int(42)
            value.get_int()
            value.unset()
            value = GObject.Value()
            value.init(GObject.TYPE_STRING)
            value.set_string("foobar")
            value.get_string()
            value.unset()
            value = GObject.Value()
            value.init(GObject.TYPE_OBJECT)
            value.set_object(b)
            value.get_object()
            value.unset()
            t = time.time() - t
            times.append(t)
        return times

    def bench_object(n):
        times = []
        for i in xrange(n):
            t = time.time()
            w = Gtk.Window()
            w.props.title = "this"
            t = time.time() - t
            times.append(t)
        return times

    def bench_method(n):
        times = []
        b = Gtk.Button()
        for i in xrange(n):
            t = time.time()
            b.set_name("foobar")
            b.get_name()
            b.set_relief(Gtk.ReliefStyle.NORMAL)
            b.get_relief()
            b.set_use_stock(True)
            b.get_use_stock()
            b.set_alignment(0.2, 0.4)
            b.get_alignment()
            t = time.time() - t
            times.append(t)
        return times

    def torture_signature_0(rounds):
        test = Regress.TestObj()
        func = test.torture_signature_0
        times = []
        for i in xrange(rounds):
            t0 = time.time()
            func(5000, "foobar", 12345)
            times.append(time.time() - t0)
        return times

    def torture_signature_1(rounds):
        test = Regress.TestObj()
        func = test.torture_signature_1
        times = []
        for i in xrange(rounds):
            t0 = time.time()
            func(5000, "foobar", 12344)
            times.append(time.time() - t0)
        return times

    def torture_signature_1e(rounds):
        test = Regress.TestObj()
        func = test.torture_signature_1
        times = []
        for i in xrange(rounds):
            t0 = time.time()
            try:
                func(5000, "foobar", 12345)
            except:
                pass
            times.append(time.time() - t0)
        return times

    bench = [
        (bench_func, 10000),
        (bench_method, 10000),
        (bench_gvalue, 1000),
        (bench_object, 1000),
    ]

    try:
        from gi.repository import Regress
    except ImportError:
        pass
    else:
        bench.extend([
            (torture_signature_0, 10000),
            (torture_signature_1, 10000),
            (torture_signature_1e, 10000),
        ])

    for b, n in bench:
        min_time = min(b(n))
        print("%20s: %5.2f µs" % (b.__name__, min_time * (10 ** 6)))
