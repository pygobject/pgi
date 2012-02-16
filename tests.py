# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest
from gitypes import *
from ctypes import *

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


if __name__ == '__main__':
    gi_init()
    unittest.main()
