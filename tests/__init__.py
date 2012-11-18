# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import unittest


def test(load_gi):
    """Run the test suite.

    gi -- run all tests in the pygobject suite with PyGObject

    """

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

    current_dir = os.path.join(os.path.dirname(__file__))

    suites = []

    loader = unittest.TestLoader()
    suites.append(loader.discover(os.path.join(current_dir, "pygobject")))

    if not load_gi:
        loader = unittest.TestLoader()
        suites.append(loader.discover(os.path.join(current_dir, "gir")))

    run = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))
    return len(run.failures) + len(run.errors)
