# Copyright 2013 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os
import glob
import sys
import subprocess
import unittest

os.environ["PYFLAKES_NODOCTEST"] = "1"
try:
    from pyflakes.scripts import pyflakes
except ImportError:
    pyflakes = None


class FakeStream(object):
    # skip these, can be false positives
    BL = ["imported but unused",
          #"redefinition of unused",
          "unable to detect undefined names",
          "redefinition of function"]

    def __init__(self):
        self.lines = []

    def write(self, text):
        for p in self.BL:
            if p in text:
                return
        text = text.strip()
        if not text:
            return
        self.lines.append(text)

    def check(self):
        if self.lines:
            raise Exception("\n" + "\n".join(self.lines))


@unittest.skipUnless(pyflakes, "no pyflakes found")
class TPyFlakes(unittest.TestCase):

    def _run(self, path):
        old_stdout = sys.stdout
        stream = FakeStream()
        try:
            sys.stdout = stream
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.py'):
                        pyflakes.checkPath(os.path.join(dirpath, filename))
        finally:
            sys.stdout = old_stdout
        stream.check()

    def _run_package(self, mod):
        path = mod.__path__[0]
        self._run(path)

    def test_main(self):
        import pgi
        self._run_package(pgi)
