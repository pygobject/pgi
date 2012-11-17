# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest
from ctypes import byref, cast

from pgi.gir import *
from pgi.gobject import *
from pgi.glib import *


class GITypesTest(unittest.TestCase):

    def setUp(self):
        repo = GIRepository.get_default()
        repo.require("Gtk", "3.0", 0, byref(GErrorPtr()))
        infos = {}
        for i in xrange(repo.get_n_infos("Gtk")):
            info = repo.get_info("Gtk", i)
            infos[info.get_name()] = info

        self.infos = infos

    def tearDown(self):
        for v in self.infos.itervalues():
            v.unref()
        del self.infos

    def test_baseinfo(self):
        b = self.infos["Button"]
        repr(b)
        b.ref()
        b.unref()
        self.failUnlessEqual(b.get_name(), "Button")
        self.failUnlessEqual(b.get_namespace(), "Gtk")
        self.failUnlessEqual(b.is_deprecated(), False)
        self.failIf(b.get_container())
        self.failUnlessEqual(b.get_type().value, GIInfoType.OBJECT)
        repr(b.get_typelib())

    def test_typelib(self):
        w = self.infos["Window"]
        t = w.get_typelib()
        repr(t)
        self.failUnlessEqual(t.get_namespace(), "Gtk")

    def test_objectinfo(self):
        e = self.infos["Expander"]
        e = cast(e, GIObjectInfoPtr)
        repr(e)
        self.failUnlessEqual(e.get_type_name(), "GtkExpander")
        self.failUnlessEqual(e.get_type_init(), "gtk_expander_get_type")

    def test_enuminfo(self):
        t = self.infos["WindowType"]
        t = cast(t, GIEnumInfoPtr)
        repr(t)
        self.failUnlessEqual(t.get_n_methods(), 0)
        self.failUnlessEqual(t.get_storage_type().value, GITypeTag.UINT32)
        self.failUnlessEqual(t.get_value(0).get_value(), 0)

    def test_functioninfo(self):
        e = self.infos["Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(10)
        repr(fi)
        self.failUnlessEqual(fi.get_symbol(), "gtk_expander_set_expanded")
        self.failUnlessEqual(fi.get_flags().value,
                             GIFunctionInfoFlags.IS_METHOD)
        fi.unref()

    def test_callableinfo(self):
        e = self.infos["Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(9)
        ci = cast(fi, GICallableInfoPtr)
        repr(ci)
        fi.unref()

    def test_interfaceinfo(self):
        i = self.infos["Editable"]
        i = cast(i, GIInterfaceInfoPtr)
        repr(i)
