# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import unittest

from pgi._compat import PY3


class _GIRepoTest(unittest.TestCase):

    GIRepository = None
    GIError = None
    gir = None
    gobject = None

    def test_repository(self):
        repo = self.GIRepository.get_default()
        self.assertTrue(isinstance(repo, self.GIRepository))

    def test_require_invalid(self):
        repo = self.GIRepository.get_default()
        self.assertRaises(self.GIError, repo.require, "Gtk", "999.0", 0)

        try:
            repo.require("Gtk", "999.0", 0)
        except self.GIError as e:
            self.assertTrue(isinstance(e.message, str))

    def test_require_latest(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", None, 0)

    def test_require_private_latest(self):
        repo = self.GIRepository.get_default()
        # require first, so require_private doesn't do anything
        repo.require("GObject", "2.0", 0)
        repo.require_private(b"/nope", "GObject", None, 0)

    def test_enumerate_versions(self):
        repo = self.GIRepository.get_default()
        self.assertEqual(repo.enumerate_versions("Foobar999"), [])
        self.assertTrue("2.0" in repo.enumerate_versions("GObject"))

    def test_get_loaded_namespaces(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        res = repo.get_loaded_namespaces()
        self.assertTrue(isinstance(res, list))
        self.assertTrue("GObject" in res)

    def test_get_immediate_dependencies(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertEqual(
            repo.get_immediate_dependencies("GObject"), ["GLib-2.0"])

    def test_search_path(self):
        repo = self.GIRepository.get_default()
        repo.prepend_search_path(b"/nope")
        self.assertEqual(repo.get_search_path()[0], "/nope")

    def test_prepend_library_path(self):
        repo = self.GIRepository.get_default()
        try:
            repo.prepend_library_path(b"/nope")
        except AttributeError:
            # too old libgirepository
            pass

    def test_find_by_name(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        res = repo.find_by_name("GObject", "Object")
        self.assertTrue(isinstance(res, self.gir.GIObjectInfo))

        res = repo.find_by_name("GObject", "Foobar")
        self.assertTrue(res is None)

    def test_find_by_gtype(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        gtype = self.gobject.GType.from_name(b"GObject")
        self.assertTrue(gtype)
        res = repo.find_by_gtype(gtype)
        self.assertTrue(isinstance(res, self.gir.GIObjectInfo))

    def test_is_registered(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        res = repo.is_registered("GObject", "2.0")
        self.assertTrue(res)
        res = repo.is_registered("GObject", None)
        self.assertTrue(res)
        res = repo.is_registered("GObject")
        self.assertTrue(res)
        res = repo.is_registered("Foobar", "2.0")
        self.assertFalse(res)

    def test_get_n_infos(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertTrue(repo.get_n_infos("GObject") > 10)

    def test_get_info(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        res = repo.get_info("GObject", 0)
        self.assertTrue(isinstance(res, self.gir.GIBaseInfo))

    def test_get_infos(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        for res in repo.get_infos("GObject"):
            self.assertTrue(isinstance(res, self.gir.GIBaseInfo))
            break

    def test_get_typelib_path(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertTrue(os.path.exists(repo.get_typelib_path("GObject")))

        path = repo.get_typelib_path("GObject")
        if PY3:
            self.assertTrue(isinstance(path, str))
        elif os.name == "nt":
            self.assertTrue(isinstance(path, unicode))
        else:
            self.assertTrue(isinstance(path, bytes))

        self.assertTrue(repo.get_typelib_path("NopeNope") is None)

    def test_get_shared_library(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertTrue("gobject" in repo.get_shared_library("GObject"))

    def test_get_version(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertEqual(repo.get_version("GObject"), "2.0")

    def test_get_c_prefix(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        self.assertEqual(repo.get_c_prefix("GObject"), "G")

    def test_typelib_from_memory_error(self):
        self.assertRaises(
            self.GIError, self.gir.GITypelib.new_from_memory, b"foo")

    def test_typelib_from_memory_load_typelib(self):
        repo = self.GIRepository.get_default()
        repo.require("GObject", "2.0", 0)
        path = repo.get_typelib_path("GObject")
        with open(path, "rb") as h:
            data = h.read()
        typelib = self.gir.GITypelib.new_from_memory(data)
        self.assertEqual(repo.load_typelib(typelib, 0), "GObject")


class GIRepoTestCTypes(_GIRepoTest):
    from pgi.clib import gir, gobject
    from pgi.clib.gir import GIRepository
    from pgi.clib.gir import GIError

    GIRepository, GIError, gir, gobject


class GIRepoTestCFFI(_GIRepoTest):
    from pgi.cffilib import gir, gobject
    from pgi.cffilib.gir import GIRepository
    from pgi.cffilib.gir import GIError

    GIRepository, GIError, gir, gobject
