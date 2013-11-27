# Copyright 2013 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os
import glob
import subprocess
import unittest


PEP8_NAME = "pep8"


has_pep8 = True
try:
    subprocess.check_output([PEP8_NAME, "--version"], stderr=subprocess.STDOUT)
except OSError:
    has_pep8 = False


@unittest.skipUnless(has_pep8, "no pep8")
class TPEP8(unittest.TestCase):
    # don't care..
    IGNORE_ERROROS = "E12,E261,W603"
    PACKAGES = []

    def _run(self, path):
        p = subprocess.Popen(
            [PEP8_NAME, "--ignore=" + self.IGNORE_ERROROS, path],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if p.wait() != 0:
            o, e = p.communicate()
            raise Exception("\n" + o)

    def test_main_package(self):
        import gi
        path = gi.__path__[0]
        files = glob.glob(os.path.join(path, "*.py"))
        assert files
        for file_ in files:
            self._run(file_)

    def test_repository(self):
        import gi.repository
        path = gi.repository.__path__[0]
        files = glob.glob(os.path.join(path, "*.py"))
        assert files
        for file_ in files:
            self._run(file_)

    def test_codegen(self):
        import gi.codegen
        path = gi.codegen.__path__[0]
        files = glob.glob(os.path.join(path, "*.py"))
        assert files
        for file_ in files:
            self._run(file_)

    def test_clib(self):
        import gi.clib
        path = gi.clib.__path__[0]
        files = glob.glob(os.path.join(path, "*.py"))
        assert files
        for file_ in files:
            self._run(file_)
