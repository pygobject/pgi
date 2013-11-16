# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi._compat import StringIO

from pgi.codegen import ctypes_backend
try:
    from pgi.codegen import cffi_backend
    cffi_backend = cffi_backend
except ImportError:
    cffi_backend = None
from pgi.util import escape_name, unescape_name, escape_builtin
from pgi.codegen.utils import CodeBlock, parse_code
from pgi.gtype import PGType
from pgi.clib.gobject import GType


class PGIMisc(unittest.TestCase):
    def test_escape_property(self):
        self.assertEqual(escape_name("class"), "class_")
        self.assertEqual(escape_name("cla-ss"), "cla_ss")
        self.assertEqual(escape_name("2BUTTON_PRESS"), "_2BUTTON_PRESS")

    def test_unescape_property(self):
        self.assertEqual(unescape_name("foo_"), "foo")
        self.assertEqual(unescape_name("fo_oo"), "fo-oo")

    def test_escape_builtin(self):
        self.assertEqual(escape_builtin("type"), "type_")
        self.assertEqual(escape_builtin("all"), "all_")

    def test_codeblock(self):
        a = CodeBlock("foo")
        self.assertEqual(str(a), "foo")
        a.write_lines(["1", "2"], 0)
        self.assertEqual(str(a), "foo\n1\n2")

    def test_codeblock_deps(self):
        a = CodeBlock()
        a.add_dependency("a", object())
        self.assertRaises(ValueError, a.add_dependency, "a", object())

    def test_codeblock_print(self):
        f = StringIO()
        a = CodeBlock()
        a.write_line("abc")
        a.pprint(f)
        self.assertEqual(f.getvalue(), "abc")

    def test_parse_codeblock(self):
        b = CodeBlock()
        b.add_dependency("test", "blah")
        b.write_line("if 1:")
        b.write_line("do()", 1)
        n, v = parse_code("""
if 2:
    $doit
""", None, doit=b)

        self.assertEqual(str(n), "if 2:\n    if 1:\n        do()")
        self.assertTrue("test" in n.get_dependencies())

    def test_gtype(self):
        self.assertEqual(PGType(0), PGType(GType(0)))

    @unittest.skipUnless(cffi_backend, "")
    def test_backends(self):
        # to keep things simple the cffi backend should be a subset
        # of the ctypes one. So check all attributes
        cffi = [a for a in dir(cffi_backend.CFFIBackend) if a[:1] != "_"]
        ct = [a for a in dir(ctypes_backend.CTypesBackend) if a[:1] != "_"]
        self.assertFalse(set(cffi) - set(ct))

    def test_docstring(self):
        from pgi.repository import Gtk
        self.assertTrue("get_label" in Gtk.Button.get_label.__doc__)
        self.assertTrue("-> str" in Gtk.Button.get_label.__doc__)
        self.assertTrue("set_label" in Gtk.Button.set_label.__doc__)
        self.assertTrue("-> None" in Gtk.Button.set_label.__doc__)
        self.assertTrue("label: str" in Gtk.Button.set_label.__doc__)

    def test_signal_property_object(self):
        from pgi.repository import Gtk
        sigs = Gtk.Window.signals
        sig = sigs.set_focus
        self.assertEqual(sig.name, "set-focus")
        self.assertEqual(sig.param_types, [Gtk.Widget.__gtype__])
        self.assertEqual(sig.instance_type, Gtk.Window.__gtype__)
        self.assertEqual(sig.flags, 2)
        self.assertEqual(sig.return_type, PGType.from_name("void"))

    def test_signal_property_interface(self):
        from pgi.repository import Gtk
        sigs = Gtk.TreeModel.signals
        sig = sigs.row_changed
        self.assertEqual(sig.name, "row-changed")
        # TreePath gtypes fail here.. no idea
        self.assertEqual(len(sig.param_types), 2)
        self.assertEqual(sig.instance_type, Gtk.TreeModel.__gtype__)
        self.assertEqual(sig.flags, 2)
        self.assertEqual(sig.return_type, PGType.from_name("void"))
