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
    IGNORE = ["E12", "E261"]
    PACKAGES = []

    def _run(self, path, ignore=None):
        if ignore is None:
            ignore = []
        ignore += self.IGNORE

        p = subprocess.Popen(
            [PEP8_NAME, "--ignore=" + ",".join(ignore), path],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if p.wait() != 0:
            o, e = p.communicate()
            raise Exception("\n" + o)

    def _run_package(self, mod, ignore=None):
        path = mod.__path__[0]
        files = glob.glob(os.path.join(path, "*.py"))
        assert files
        for file_ in files:
            self._run(file_, ignore)

    def test_main_package(self):
        import gi
        self._run_package(gi)

    def test_overrides(self):
        import gi.overrides
        self._run_package(
            gi.overrides, ignore=["E501", "E303", "E502", "E302"])

    def test_repository(self):
        import gi.repository
        self._run_package(gi.repository)

    def test_codegen(self):
        import gi.codegen
        self._run_package(gi.codegen)

    def test_clib(self):
        import gi.clib
        self._run_package(gi.clib)

    def test_clib_gir(self):
        import gi.clib.gir
        self._run_package(gi.clib.gir)

    def test_clib_gir(self):
        import gi.clib.gir
        self._run_package(gi.clib.gir)
