# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest
from ctypes import byref, cast

from pgi._compat import xrange
from pgi.clib.gir import *
from pgi.clib.gobject import *
from pgi.clib.glib import *


class GITypesTest(unittest.TestCase):

    def setUp(self):
        repo = GIRepository.get_default()
        repo.require(b"Gtk", b"3.0", 0, byref(GErrorPtr()))
        gtk = {}
        for i in xrange(repo.get_n_infos(b"Gtk")):
            info = repo.get_info(b"Gtk", i)
            gtk[info.name] = info

        self.gtk = gtk

        repo.require(b"Gdk", b"3.0", 0, byref(GErrorPtr()))
        gdk = {}
        for i in xrange(repo.get_n_infos(b"Gdk")):
            info = repo.get_info(b"Gdk", i)
            gdk[info.name] = info

        self.gdk = gdk

    def tearDown(self):
        del self.gtk
        del self.gdk

    def test_baseinfo(self):
        b = self.gtk[b"Button"]
        repr(b)
        self.failUnlessEqual(b.name, b"Button")
        self.failUnlessEqual(b.namespace, b"Gtk")
        self.failUnlessEqual(b.is_deprecated, False)
        self.failIf(b.get_container())
        self.failUnlessEqual(b.type.value, GIInfoType.OBJECT)
        repr(b.get_typelib())

    def test_typelib(self):
        w = self.gtk[b"Window"]
        t = w.get_typelib()
        repr(t)
        self.failUnlessEqual(t.namespace, b"Gtk")

    def test_objectinfo(self):
        e = self.gtk[b"Expander"]
        self.assertTrue(isinstance(e, GIObjectInfo))
        repr(e)
        self.failUnlessEqual(e.type_name, b"GtkExpander")
        self.failUnlessEqual(e.type_init, b"gtk_expander_get_type")

        e.get_methods()
        e.get_fields()
        e.get_interfaces()
        e.get_properties()
        e.get_signals()
        e.get_vfuncs()
        e.get_constants()

    def test_enuminfo(self):
        t = self.gtk[b"WindowType"]
        self.assertTrue(isinstance(t, GIEnumInfo))
        repr(t)
        self.failUnlessEqual(t.n_methods, 0)
        self.failUnlessEqual(t.storage_type.value, GITypeTag.UINT32)
        self.failUnlessEqual(t.get_value(0).value_, 0)

        t.get_values()
        t.get_methods()

    def test_unioninfo(self):
        e = self.gdk[b"Event"]
        self.assertTrue(isinstance(e, GIUnionInfo))
        repr(e)

        e.get_methods()
        e.get_fields()

    def test_valueinfo(self):
        t = self.gtk[b"WindowType"]
        self.assertTrue(isinstance(t, GIEnumInfo))
        v = t.get_value(0)
        repr(v)

    def test_functioninfo(self):
        e = self.gtk[b"Expander"]
        self.assertTrue(isinstance(e, GIObjectInfo))
        fi = e.get_method(10)
        self.assertTrue(isinstance(fi, GIFunctionInfo))
        repr(fi)
        self.failUnlessEqual(fi.symbol, b"gtk_expander_set_expanded")
        self.failUnlessEqual(fi.flags.value,
                             GIFunctionInfoFlags.IS_METHOD)

        w = self.gtk[b"Window"]
        self.assertTrue(isinstance(w, GIObjectInfo))
        for i in xrange(w.n_methods):
            fi = w.get_method(i)
            repr(fi)

    def test_structinfo(self):
        s = self.gtk[b"TargetEntry"]
        self.assertTrue(isinstance(s, GIStructInfo))
        s.get_fields()
        repr(s)

    def test_fieldinfo(self):
        s = self.gtk[b"TargetEntry"]
        self.assertTrue(isinstance(s, GIStructInfo))
        f = s.get_field(0)
        self.assertTrue(isinstance(f, GIFieldInfo))
        repr(f)

    def test_callableinfo(self):
        e = self.gtk[b"Expander"]
        self.assertTrue(isinstance(e, GIObjectInfo))
        fi = e.get_method(9)
        self.assertTrue(isinstance(fi, GICallableInfo))
        repr(fi)

    def test_interfaceinfo(self):
        i = self.gtk[b"Editable"]
        self.assertTrue(isinstance(i, GIInterfaceInfo))
        repr(i)

        i.get_methods()
        i.get_properties()
        i.get_signals()
        i.get_constants()
        i.get_prerequisites()
        i.get_vfuncs()

    def test_vfuncinfo(self):
        i = self.gtk[b"Editable"]
        self.assertTrue(isinstance(i, GIInterfaceInfo))
        for x in xrange(i.n_vfuncs):
            v = i.get_vfunc(x)
            self.assertTrue(isinstance(v, GIVFuncInfo))
            repr(v)

    def test_signalinfo(self):
        i = self.gtk[b"Editable"]
        self.assertTrue(isinstance(i, GIInterfaceInfo))
        for x in xrange(i.n_signals):
            v = i.get_signal(x)
            self.assertTrue(isinstance(v, GISignalInfo))
            repr(v)

    def test_propertyinfo(self):
        e = self.gtk[b"Expander"]
        self.assertTrue(e, GIObjectInfo)
        p = e.get_property(0)
        self.assertTrue(e, GIPropertyInfo)
        repr(p)

    def test_constantinfo(self):
        c = self.gtk[b"STOCK_ABOUT"]
        self.assertTrue(isinstance(c, GIConstantInfo))
        repr(c)

    def test_typeinfo(self):
        fi = GIRepository().find_by_name(b"Gtk", b"get_major_version")
        self.assertTrue(isinstance(fi, GICallableInfo))
        rt = fi.get_return_type()
        self.assertTrue(isinstance(rt, GITypeInfo))

        fi = GIRepository().find_by_name(b"Gtk", b"init")
        self.assertTrue(isinstance(fi, GICallableInfo))
        argv = fi.get_arg(1)
        repr(argv)

    def test_typetag(self):
        self.failIf(GITypeTag(18).is_basic())
        self.failUnless(GITypeTag(21).is_basic())
        self.failUnless(GITypeTag(10).is_basic())

    def test_repository(self):
        x = GIRepository.get_default()
        self.assertTrue(isinstance(x, GIRepository))
