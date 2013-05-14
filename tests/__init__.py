# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import unittest
import logging
import platform


is_gi = False
is_pypy = False
has_cairo = False

def test(load_gi, backend=None, strict=False, filter_=None):
    """Run the test suite.

    load_gi -- run all tests in the pygobject suite with PyGObject
    backend -- "ctypes" or "cffi"
    strict  -- fail on glib warnings
    filter_ -- filter for test names (class names)
    """

    global is_gi, is_pypy, has_cairo
    is_gi = load_gi
    is_pypy = platform.python_implementation() == "PyPy"

    if not load_gi:
        import pgi
        pgi.install_as_gi()
        try:
            pgi.set_backend(backend)
        except LookupError:
            print "Couldn't load backend: %r" % backend
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
    print hl[:80]

    if load_gi:
        has_cairo = True
    else:
        gi.check_foreign("cairo", "Context")

    # gi uses logging
    logging.disable(logging.ERROR)

    if strict:
        # make glib warnings fatal
        from gi.repository import GLib
        GLib.log_set_always_fatal(
            GLib.LogLevelFlags.LEVEL_CRITICAL |
            GLib.LogLevelFlags.LEVEL_ERROR |
            GLib.LogLevelFlags.LEVEL_WARNING)

    current_dir = os.path.join(os.path.dirname(__file__))

    tests = []

    loader = unittest.TestLoader()
    tests.extend(loader.discover(os.path.join(current_dir, "pygobject")))

    if not load_gi:
        loader = unittest.TestLoader()
        tests.extend(loader.discover(os.path.join(current_dir, "pgi")))

    def flatten_tests(suites):
        tests = []
        try:
            for suite in suites:
                tests.extend(flatten_tests(suite))
        except TypeError:
            return [suites]
        return tests

    tests = flatten_tests(tests)
    if filter_ is not None:
        tests = filter(lambda t: filter_(t.__class__.__name__), tests)

    run = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))
    return len(run.failures) + len(run.errors)
