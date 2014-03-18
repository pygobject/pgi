# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest


class _GIRepoTest(unittest.TestCase):

    GIRepository = None
    GIError = None

    def test_repository(self):
        repo = self.GIRepository.get_default()
        self.assertTrue(isinstance(repo, self.GIRepository))

    def test_require_invalid(self):
        repo = self.GIRepository.get_default()
        self.assertRaises(self.GIError, repo.require, b"Gtk", b"999.0", 0)

    def test_enumerate_versions(self):
        repo = self.GIRepository.get_default()
        self.assertEqual(repo.enumerate_versions("Foobar999"), [])
        self.assertTrue("2.0" in repo.enumerate_versions("GObject"))


class GIRepoTestCTypes(_GIRepoTest):
    from pgi.clib.gir import GIRepository
    from pgi.clib.gir import GIError


class GIRepoTestCFFI(_GIRepoTest):
    from pgi.cffilib.gir import GIRepository
    from pgi.cffilib.gir import GIError
