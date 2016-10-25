# Copyright 2012,2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest
import sys
import os

from tests import skipIfGI

import gi
from gi import get_required_version, require_version, PyGIDeprecationWarning
require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib, Gdk
from pgi import _compat


class MiscTest(unittest.TestCase):

    def test_deprecation_warning(self):
        self.assertTrue(issubclass(PyGIDeprecationWarning, DeprecationWarning))

    def test_module_dir(self):
        # make sure all descriptors show up in dir(module)
        self.assertTrue(len(dir(Gtk)) > 750)

        if _compat.PY2:
            self.assertEqual(sys.getdefaultencoding(), "ascii")
        else:
            self.assertEqual(sys.getdefaultencoding(), "utf-8")

        self.assertEqual(Gtk._version, "3.0")
        self.assertEqual(GObject._version, "2.0")
        self.assertEqual(GLib._version, "2.0")

    def test_require_version(self):
        self.assertTrue(require_version("Gtk", "3.0") is None)
        self.assertRaises(ValueError, require_version, "Gtk", "4.0")
        self.assertRaises(ValueError, require_version, "Gtk", "2.0")
        self.assertEqual(get_required_version("Gtk"), "3.0")
        self.assertTrue(get_required_version("...") is None)
        self.assertRaises(ValueError, require_version, "...", "3.0")

    def test_import(self):
        self.assertRaises(ImportError, __import__,
                          "gi.repository.FooBar", fromlist=[""])

    def test_module(self):
        self.assertTrue(Gtk.__path__.endswith(".typelib"))
        self.assertTrue(Gtk.__loader__)
        self.assertTrue(Gtk.__file__.endswith(".repository.Gtk>"))

    def test_structure(self):
        a = Gdk.atom_intern('CLIPBOARD', True)
        self.assertTrue(isinstance(a, Gdk.Atom))
        self.assertTrue(isinstance(Gtk.Clipboard.get(a), Gtk.Clipboard))
        self.assertRaises(TypeError, Gtk.Clipboard.get, None)
        self.assertRaises(TypeError, Gtk.Clipboard.get, 0)
        self.assertRaises(TypeError, Gtk.Clipboard.get, Gdk.Atom)
        self.assertRaises(TypeError, Gdk.Atom, "baz")

    def test_pygi_atom(self):
        atom = Gdk.Atom.intern('my_string', False)
        self.assertEqual(atom.name(), 'my_string')
        a_selection = Gdk.Atom.intern('test_clipboard', False)
        clipboard = Gtk.Clipboard.get(a_selection)
        clipboard.set_text('hello', 5)
        self.assertRaises(TypeError, Gtk.Clipboard.get, 'CLIPBOARD')

    @skipIfGI
    def test_base_types_class(self):
        c = GObject.GError
        self.assertTrue("GLib" in c.__module__)
        self.assertTrue("Error" in c.__name__)

        c = GObject.GFlags
        self.assertTrue("GObject" in c.__module__)
        self.assertTrue("GFlags" in c.__name__)

        c = GObject.GEnum
        self.assertTrue("GObject" in c.__module__)
        self.assertTrue("GEnum" in c.__name__)

        c = GObject.GInterface
        self.assertTrue("GObject" in c.__module__)
        self.assertTrue("GInterface" in c.__name__)

    @skipIfGI
    def test_override_new_class(self):
        c = Gdk.EventProperty
        self.assertTrue("override" not in c.__module__)
        self.assertTrue("Gdk" in c.__module__)
        self.assertTrue("EventProperty" in c.__name__)

    def test_gerror(self):
        self.assertTrue(issubclass(GLib.GError, RuntimeError))

    @unittest.skipIf(_compat.PY3, "py3")
    def test_param_flags_32_64(self):
        if sys.maxint == 2**31-1:
            self.assertEqual(int(GObject.ParamFlags.DEPRECATED), -2147483648)
        else:
            # FIXME: pygobject gets 2147483648, we get -2147483648
            #self.assertEqual(int(GObject.ParamFlags.DEPRECATED), 2147483648)
            pass

    def test_module_special_methods(self):
        if os.name == "nt":
            self.assertTrue(isinstance(Gtk.__path__, type(u"")))
        else:
            self.assertTrue(isinstance(Gtk.__path__, str))

    @unittest.skipIf(_compat.PY3, "py3")
    def test_vfunc_name_escape(self):
        # print only a keyword in py2
        try:
            gi.require_version('WebKit2', '4.0')
            from gi.repository import WebKit2
        except (ImportError, ValueError):
            return

        # pygobject escapes vfuncs before prefixing, do the same
        self.assertTrue(hasattr(WebKit2.WebView, "do_print_"))

    @unittest.skipUnless(hasattr(gi, "require_foreign"), "too old gi")
    def test_check_foreign(self):
        self.assertRaises(ImportError, gi.require_foreign, "foo", "bar")
        self.assertRaises(ImportError, gi.require_foreign, "foo")
