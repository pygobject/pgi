# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest
from gitypes import *
from ctypes import *

def glist_get_all(g, type_):
    values = []
    while g:
        value = cast(g.contents.data, type_).value
        values.append(value)
        g = g.next()
    return values

def get_ptr_list(x):
    if not x: return
    i = 0
    while 1:
        val = x[i]
        if val is None:
            return
        yield x[i]
        i += 1

class TestBaseInfo(unittest.TestCase):
    def setUp(self):
        repo = GIRepository.get_default()
        error = POINTER(GError)()
        repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY, byref(error))
        check_gerror(error)
        self.b = repo.find_by_name("GLib", "warn_message")
        self.failUnless(self.b)

    def test_base_info(self):
        b = self.b

        b.ref()
        b.unref()

        self.failUnlessEqual(b.get_type().value, GIInfoType.FUNCTION)
        self.failUnlessEqual(b.get_name(), "warn_message")
        self.failUnlessEqual(b.get_namespace(), "GLib")
        self.failUnlessEqual(b.is_deprecated(), False)

        iter_ = GIAttributeIter()
        name = c_char_p()
        value = c_char_p()
        more = b.iterate_attributes(byref(iter_), byref(name), byref(value))
        self.failUnlessEqual(more, False)

        self.failIf(b.get_attribute(gchar_p("foo")))

        self.failIf(b.get_container())

        self.failUnless(b.get_typelib())
        self.failUnless(b.equal(b))

    def test_info_type(self):
        self.failUnlessEqual(
            GIInfoType.to_string(GIInfoType.INVALID), "invalid")
        self.failUnlessEqual(
            GIInfoType.to_string(GIInfoType.UNRESOLVED), "unresolved")

    def tearDown(self):
        self.b.unref()


class TestTypeLib(unittest.TestCase):
    def setUp(self):
        repo = GIRepository.get_default()
        error = POINTER(GError)()
        self.tl = repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY,
                               byref(error))
        check_gerror(error)
        self.failUnless(self.tl)

    def test_typelib(self):
        self.failUnlessEqual(self.tl.get_namespace(), "GLib")

        symbol = gpointer()
        self.tl.symbol(gchar_p(""), byref(symbol))

        self.tl.free()

    def test_new(self):
        error = GErrorPtr()
        data = guint8()
        GITypelib.new_from_memory(byref(data), 0, byref(error))
        error.free()

        error = GErrorPtr()
        GITypelib.new_from_const_memory(byref(data), 0, byref(error))
        error.free()

        error = GErrorPtr()
        mf = GMappedFile()
        GITypelib.new_from_mapped_file(byref(mf), byref(error))
        error.free()


class TestGIR(unittest.TestCase):
    def test(self):
        repo = GIRepository.get_default()
        error = GErrorPtr()
        repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY, byref(error))
        check_gerror(error)

        libs = repo.get_shared_library("GLib").split(",")
        self.failUnless("libglib-2.0.so.0" in libs)

        self.failUnlessEqual(repo.get_version("GLib"), "2.0")

        GIRepository.get_option_group()

        self.failUnlessEqual(repo.get_c_prefix("GLib"), "G")

        glist = repo.enumerate_versions("GLib")
        versions = glist_get_all(glist, gchar_p)
        self.failUnless("2.0" in versions)

        path = repo.get_typelib_path("GLib")
        self.failUnless("GLib-2.0.typelib" in path)

        ns = repo.get_loaded_namespaces()
        self.failUnless("GLib" in get_ptr_list(ns))

        deps = repo.get_dependencies("GLib")
        self.failIf(list(get_ptr_list(deps)))

        glist = GIRepository.get_search_path()
        values = glist_get_all(glist, c_char_p)
        self.failUnless(values)
        path = values[0]

        error = POINTER(GError)()
        repo.require_private(path, "GObject", "2.0",
                             GIRepositoryLoadFlags.LAZY, byref(error))
        check_gerror(error)

        deps = get_ptr_list(repo.get_dependencies("GObject"))
        self.failUnless("GLib-2.0" in deps)

        self.failUnless(repo.is_registered("GLib", "2.0"))

        GIRepository.prepend_search_path("foo")

        glist = GIRepository.get_search_path()
        values = glist_get_all(glist, c_char_p)
        self.failUnless("foo" in values)

if __name__ == '__main__':
    gi_init()
    unittest.main()
