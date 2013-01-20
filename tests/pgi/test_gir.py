# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest
from ctypes import byref, cast

from pgi.gir import *
from pgi.gobject import *
from pgi.glib import *


class GITypesTest(unittest.TestCase):

    def setUp(self):
        repo = GIRepository.get_default()
        repo.require("Gtk", "3.0", 0, byref(GErrorPtr()))
        gtk = {}
        for i in xrange(repo.get_n_infos("Gtk")):
            info = repo.get_info("Gtk", i)
            gtk[info.name] = info

        self.gtk = gtk

        repo.require("Gdk", "3.0", 0, byref(GErrorPtr()))
        gdk = {}
        for i in xrange(repo.get_n_infos("Gdk")):
            info = repo.get_info("Gdk", i)
            gdk[info.name] = info

        self.gdk = gdk

    def tearDown(self):
        for v in self.gtk.itervalues():
            v.unref()
        del self.gtk
        for v in self.gdk.itervalues():
            v.unref()
        del self.gdk

    def test_baseinfo(self):
        b = self.gtk["Button"]
        repr(b)
        b.ref()
        b.unref()
        self.failUnlessEqual(b.name, "Button")
        self.failUnlessEqual(b.namespace, "Gtk")
        self.failUnlessEqual(b.is_deprecated, False)
        self.failIf(b.get_container())
        self.failUnlessEqual(b.type.value, GIInfoType.OBJECT)
        repr(b.get_typelib())

    def test_typelib(self):
        w = self.gtk["Window"]
        t = w.get_typelib()
        repr(t)
        self.failUnlessEqual(t.namespace, "Gtk")

    def test_objectinfo(self):
        e = self.gtk["Expander"]
        self.failUnless(gi_is_registered_type_info(e))
        self.failUnless(gi_is_object_info(e))
        e = cast(e, GIObjectInfoPtr)
        repr(e)
        self.failUnlessEqual(e.type_name, "GtkExpander")
        self.failUnlessEqual(e.type_init, "gtk_expander_get_type")

        map(lambda x: x.unref(), e.get_methods())
        map(lambda x: x.unref(), e.get_fields())
        map(lambda x: x.unref(), e.get_interfaces())
        map(lambda x: x.unref(), e.get_properties())
        map(lambda x: x.unref(), e.get_signals())
        map(lambda x: x.unref(), e.get_vfuncs())
        map(lambda x: x.unref(), e.get_constants())

    def test_enuminfo(self):
        t = self.gtk["WindowType"]
        self.failUnless(gi_is_enum_info(t))
        self.failUnless(gi_is_registered_type_info(t))
        t = cast(t, GIEnumInfoPtr)
        repr(t)
        self.failUnlessEqual(t.n_methods, 0)
        self.failUnlessEqual(t.storage_type.value, GITypeTag.UINT32)
        self.failUnlessEqual(t.get_value(0).value, 0)

        map(lambda x: x.unref(), t.get_values())
        map(lambda x: x.unref(), t.get_methods())

    def test_unioninfo(self):
        e = self.gdk["Event"]
        self.failUnless(gi_is_union_info(e))
        self.failUnless(gi_is_registered_type_info(e))
        e = cast(e, GIUnionInfoPtr)
        repr(e)

        map(lambda x: x.unref(), e.get_methods())
        map(lambda x: x.unref(), e.get_fields())

    def test_valueinfo(self):
        t = self.gtk["WindowType"]
        t = cast(t, GIEnumInfoPtr)
        v = t.get_value(0)
        self.failUnless(gi_is_value_info(cast(v, GIBaseInfoPtr)))
        repr(v)
        v.unref()

    def test_functioninfo(self):
        e = self.gtk["Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(10)
        self.failUnless(gi_is_function_info(cast(fi, GIBaseInfoPtr)))
        repr(fi)
        self.failUnlessEqual(fi.symbol, "gtk_expander_set_expanded")
        self.failUnlessEqual(fi.flags.value,
                             GIFunctionInfoFlags.IS_METHOD)
        fi.unref()

        w = self.gtk["Window"]
        w = cast(w, GIObjectInfoPtr)
        for i in xrange(w.n_methods):
            fi = w.get_method(i)
            repr(fi)
            fi.unref()

    def test_structinfo(self):
        s = self.gtk["TargetEntry"]
        self.failUnless(gi_is_struct_info(s))
        self.failUnless(gi_is_registered_type_info(s))
        s = cast(s, GIStructInfoPtr)
        map(lambda x: x.unref(), s.get_fields())
        repr(s)

    def test_fieldinfo(self):
        s = self.gtk["TargetEntry"]
        s = cast(s, GIStructInfoPtr)
        f = s.get_field(0)
        self.failUnless(gi_is_field_info(cast(f, GIBaseInfoPtr)))
        repr(f)
        f.unref()

    def test_callableinfo(self):
        e = self.gtk["Expander"]
        e = cast(e, GIObjectInfoPtr)
        fi = e.get_method(9)
        ci = cast(fi, GICallableInfoPtr)
        self.failUnless(gi_is_callable_info(cast(ci, GIBaseInfoPtr)))
        repr(ci)
        fi.unref()

    def test_interfaceinfo(self):
        i = self.gtk["Editable"]
        self.failUnless(gi_is_interface_info(i))
        self.failUnless(gi_is_registered_type_info(i))
        i = cast(i, GIInterfaceInfoPtr)
        repr(i)

        map(lambda x: x.unref(), i.get_methods())
        map(lambda x: x.unref(), i.get_properties())
        map(lambda x: x.unref(), i.get_signals())
        map(lambda x: x.unref(), i.get_constants())
        map(lambda x: x.unref(), i.get_prerequisites())

    def test_vfuncinfo(self):
        i = self.gtk["Editable"]
        i = cast(i, GIInterfaceInfoPtr)
        for x in xrange(i.n_vfuncs):
            v = i.get_vfunc(x)
            self.failUnless(gi_is_vfunc_info(cast(v, GIBaseInfoPtr)))
            repr(v)
            v.unref()

    def test_signalinfo(self):
        i = self.gtk["Editable"]
        i = cast(i, GIInterfaceInfoPtr)
        for x in xrange(i.n_signals):
            v = i.get_signal(x)
            self.failUnless(gi_is_signal_info(cast(v, GIBaseInfoPtr)))
            repr(v)
            v.unref()

    def test_propertyinfo(self):
        e = self.gtk["Expander"]
        e = cast(e, GIObjectInfoPtr)
        p = e.get_property(0)
        self.failUnless(gi_is_property_info(cast(p, GIBaseInfoPtr)))
        repr(p)
        p.unref()

    def test_constantinfo(self):
        c = self.gtk["STOCK_ABOUT"]
        self.failUnless(gi_is_constant_info(c))
        c = cast(c, GIConstantInfoPtr)
        repr(c)

    def test_typeinfo(self):
        fi = GIRepositoryPtr().find_by_name("Gtk", "get_major_version")
        fi = cast(fi, GICallableInfoPtr)
        rt = fi.get_return_type()
        self.failUnless(gi_is_type_info(cast(rt, GIBaseInfoPtr)))
        rt.unref()
        fi.unref()

        fi = GIRepositoryPtr().find_by_name("Gtk", "init")
        fi = cast(fi, GICallableInfoPtr)
        argv = fi.get_arg(1)
        self.failUnless(gi_is_arg_info(cast(argv, GIBaseInfoPtr)))
        repr(argv)
        argv.unref()
        fi.unref()

    def test_typetag(self):
        self.failIf(GITypeTag(18).is_basic())
        self.failUnless(GITypeTag(21).is_basic())
        self.failUnless(GITypeTag(10).is_basic())
