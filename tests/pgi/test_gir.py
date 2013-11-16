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
        self.failUnless(gi_is_registered_type_info(e))
        self.failUnless(gi_is_object_info(e))
        e = cast(e, GIObjectInfoPtr)
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
        self.failUnless(gi_is_enum_info(t))
        self.failUnless(gi_is_registered_type_info(t))
        t = cast(t, GIEnumInfoPtr)
        repr(t)
        self.failUnlessEqual(t.n_methods, 0)
        self.failUnlessEqual(t.storage_type.value, GITypeTag.UINT32)
        self.failUnlessEqual(t.get_value(0).value, 0)

        t.get_values()
        t.get_methods()

    def test_unioninfo(self):
        e = self.gdk[b"Event"]
        self.failUnless(gi_is_union_info(e))
        self.failUnless(gi_is_registered_type_info(e))
        e = cast(e, GIUnionInfoPtr)
        repr(e)

        e.get_methods()
        e.get_fields()

    def test_valueinfo(self):
        t = self.gtk[b"WindowType"]
        t = cast(t, GIEnumInfoPtr)
        v = t.get_value(0)
        self.failUnless(gi_is_value_info(cast(v, GIBaseInfoPtr)))
        repr(v)

    def test_functioninfo(self):
        e = self.gtk[b"Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(10)
        self.failUnless(gi_is_function_info(cast(fi, GIBaseInfoPtr)))
        repr(fi)
        self.failUnlessEqual(fi.symbol, b"gtk_expander_set_expanded")
        self.failUnlessEqual(fi.flags.value,
                             GIFunctionInfoFlags.IS_METHOD)

        w = self.gtk[b"Window"]
        w = cast(w, GIObjectInfoPtr)
        for i in xrange(w.n_methods):
            fi = w.get_method(i)
            repr(fi)

    def test_structinfo(self):
        s = self.gtk[b"TargetEntry"]
        self.failUnless(gi_is_struct_info(s))
        self.failUnless(gi_is_registered_type_info(s))
        s = cast(s, GIStructInfoPtr)
        s.get_fields()
        repr(s)

    def test_fieldinfo(self):
        s = self.gtk[b"TargetEntry"]
        s = cast(s, GIStructInfoPtr)
        f = s.get_field(0)
        self.failUnless(gi_is_field_info(cast(f, GIBaseInfoPtr)))
        repr(f)

    def test_callableinfo(self):
        e = self.gtk[b"Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(9)
        ci = cast(fi, GICallableInfoPtr)
        self.failUnless(gi_is_callable_info(cast(ci, GIBaseInfoPtr)))
        repr(ci)

    def test_interfaceinfo(self):
        i = self.gtk[b"Editable"]
        self.failUnless(gi_is_interface_info(i))
        self.failUnless(gi_is_registered_type_info(i))
        i = cast(i, GIInterfaceInfoPtr)
        repr(i)

        i.get_methods()
        i.get_properties()
        i.get_signals()
        i.get_constants()
        i.get_prerequisites()

    def test_vfuncinfo(self):
        i = self.gtk[b"Editable"]
        i = cast(i, GIInterfaceInfoPtr)
        for x in xrange(i.n_vfuncs):
            v = i.get_vfunc(x)
            self.failUnless(gi_is_vfunc_info(cast(v, GIBaseInfoPtr)))
            repr(v)

    def test_signalinfo(self):
        i = self.gtk[b"Editable"]
        i = cast(i, GIInterfaceInfoPtr)
        for x in xrange(i.n_signals):
            v = i.get_signal(x)
            self.failUnless(gi_is_signal_info(cast(v, GIBaseInfoPtr)))
            repr(v)

    def test_propertyinfo(self):
        e = self.gtk[b"Expander"]
        e = cast(e, GIObjectInfoPtr)
        p = e.get_property(0)
        self.failUnless(gi_is_property_info(cast(p, GIBaseInfoPtr)))
        repr(p)

    def test_constantinfo(self):
        c = self.gtk[b"STOCK_ABOUT"]
        self.failUnless(gi_is_constant_info(c))
        c = cast(c, GIConstantInfoPtr)
        repr(c)

    def test_typeinfo(self):
        fi = GIRepositoryPtr().find_by_name(b"Gtk", b"get_major_version")
        fi = cast(fi, GICallableInfoPtr)
        rt = fi.get_return_type()
        self.failUnless(gi_is_type_info(cast(rt, GIBaseInfoPtr)))

        fi = GIRepositoryPtr().find_by_name(b"Gtk", b"init")
        fi = cast(fi, GICallableInfoPtr)
        argv = fi.get_arg(1)
        self.failUnless(gi_is_arg_info(cast(argv, GIBaseInfoPtr)))
        repr(argv)

    def test_typetag(self):
        self.failIf(GITypeTag(18).is_basic())
        self.failUnless(GITypeTag(21).is_basic())
        self.failUnless(GITypeTag(10).is_basic())
