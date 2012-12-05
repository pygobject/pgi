# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import unittest
import logging


is_gi = False

def test(load_gi):
    """Run the test suite.

    gi -- run all tests in the pygobject suite with PyGObject

    """

    global is_gi

    if not load_gi:
        import pgi
        pgi.replace_gi()

    import gi
    if load_gi:
        is_gi = True
        assert gi.__name__ == "gi"
        print "### GI " + "#" * 61
    else:
        is_gi = False
        assert gi.__name__ == "pgi"
        print "### PGI " + "#" * 60

    # gi uses logging
    logging.disable(logging.ERROR)

    current_dir = os.path.join(os.path.dirname(__file__))

    suites = []

    loader = unittest.TestLoader()
    suites.append(loader.discover(os.path.join(current_dir, "pygobject")))

    if not load_gi:
        loader = unittest.TestLoader()
        suites.append(loader.discover(os.path.join(current_dir, "gir")))

    run = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))
    return len(run.failures) + len(run.errors)
