# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import re
import unittest

from tests import skipUnlessCairo

import pgi
from pgi._compat import StringIO

from pgi.foreign import get_foreign
from pgi.codegen import ctypes_backend
try:
    from pgi.codegen import cffi_backend
    cffi_backend = cffi_backend
except ImportError:
    cffi_backend = None
from pgi.util import escape_identifier, unescape_identifier
from pgi.util import escape_parameter, unescape_parameter
from pgi.codegen.utils import CodeBlock, parse_code, parse_with_objects
from pgi.gtype import PGType
from pgi.clib.gobject import GType


class PGIMisc(unittest.TestCase):
    def test_escape_property(self):
        self.assertEqual(escape_parameter("class"), "class_")
        self.assertEqual(escape_parameter("cla-ss"), "cla_ss")
        self.assertEqual(escape_parameter("2BUTTON_PRESS"), "_2BUTTON_PRESS")

    def test_unescape_property(self):
        self.assertEqual(unescape_parameter("foo_"), "foo")
        self.assertEqual(unescape_parameter("fo_oo"), "fo-oo")

    def test_escape_identifier(self):
        self.assertEqual(escape_identifier("class"), "class_")
        self.assertEqual(escape_identifier("2BUTTON_PRESS"), "_2BUTTON_PRESS")

    def test_unescape_identifier(self):
        self.assertEqual(unescape_identifier("foo_"), "foo")

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

    def test_parse_with_objects(self):
        some_obj = object()
        some_int = 42
        block, mapping = parse_with_objects(
            "$foo=$bar", lambda: "X", foo=some_obj, bar=some_int)

        self.assertEqual(str(block), "X=42")
        self.assertEqual(block.get_dependencies().items(), [("X", some_obj)])

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

    def test_signal_dummy_callback_doc(self):
        from pgi.repository import Gtk
        sigs = Gtk.Window.signals
        sig = sigs.set_focus

        self.assertEqual(sig.__doc__, "set_focus(object: Gtk.Widget) -> None")
        self.assertRaises(TypeError, sig)
        self.assertRaises(NotImplementedError, sig, None)

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

    def test_check_foreign(self):
        self.assertRaises(ValueError, pgi.check_foreign, "foo", "bar")

    @skipUnlessCairo
    def test_get_foreing(self):
        foreign = get_foreign("cairo", "Context")
        self.assertTrue(foreign)

    def test_check_version(self):
        # make sure the exception mentions both versions in case of an error
        self.assertRaisesRegexp(ValueError, re.escape("99.99.99"),
                                pgi.check_version, "99.99.99")

        self.assertRaisesRegexp(ValueError, re.escape(pgi.__version__),
                                pgi.check_version, "99.99.99")

    def test_doc_strings(self):
        from pgi.repository import Gtk, GLib

        self.assertEqual(Gtk.init.__doc__,
            "init(argv: [str] or None) -> argv: [str]")

        self.assertEqual(
            Gtk.accelerator_get_label.__doc__,
            "accelerator_get_label(accelerator_key: int, "
            "accelerator_mods: Gdk.ModifierType) -> str")

        self.assertEqual(
            Gtk.accelerator_get_default_mod_mask.__doc__,
            "accelerator_get_default_mod_mask() -> Gdk.ModifierType")

        self.assertEqual(
            Gtk.rc_get_default_files.__doc__,
            "rc_get_default_files() -> [str]")

        self.assertEqual(
            Gtk.target_table_new_from_list.__doc__,
            "target_table_new_from_list(list: Gtk.TargetList) -> "
            "[Gtk.TargetEntry]")

        self.assertEqual(
            Gtk.targets_include_image.__doc__,
            "targets_include_image(targets: [Gdk.Atom], writable: bool) "
            "-> bool")

        try:
            self.assertEqual(
                Gtk.init_with_args.__doc__,
                "init_with_args(argv: [str] or None, "
                "parameter_string: str or None, entries: [GLib.OptionEntry], "
                "translation_domain: str) raises -> (bool, argv: [str])")
        except:
            # Gtk+ 3.2
            self.assertEqual(
                Gtk.init_with_args.__doc__,
                "init_with_args(argv: [str] or None, "
                "parameter_string: str, entries: [GLib.OptionEntry], "
                "translation_domain: str) raises -> (bool, argv: [str])")

        self.assertEqual(
            GLib.source_remove_by_funcs_user_data.__doc__,
            "source_remove_by_funcs_user_data(funcs: GLib.SourceFuncs, "
            "user_data: object) -> bool")

        self.assertEqual(
            Gtk.FileChooser.get_filenames.__doc__,
            "get_filenames() -> [str]")

        self.assertEqual(
            Gtk.AboutDialog.drag_begin.__doc__,
            "drag_begin(targets: Gtk.TargetList, actions: Gdk.DragAction, "
            "button: int, event: Gdk.Event) -> Gdk.DragContext")

        self.assertEqual(
            Gtk.AboutDialog.set_default_icon_from_file.__doc__,
            "set_default_icon_from_file(filename: str) raises -> bool")

    def test_callback(self):
        from gi.repository import GLib, GObject

        self.assertTrue(hasattr(GLib, "SourceFunc"))
        func = GLib.SourceFunc
        self.assertEqual(func.__name__, "SourceFunc")
        self.assertEqual(func.__module__, "GLib")

        self.assertTrue(hasattr(GObject, "Callback"))
        func = GObject.Callback
        self.assertEqual(func.__name__, "Callback")
        self.assertEqual(func.__module__, "GObject")

    def test_callback_call(self):
        from gi.repository import GLib

        self.assertRaises(RuntimeError, GLib.DestroyNotify, None)
        self.assertRaises(TypeError, GLib.DestroyNotify)

    def test_callback_docstring(self):
        from gi.repository import GLib, Gtk

        string = GLib.DestroyNotify.__doc__
        self.assertEqual(string, "DestroyNotify(data: object) -> None")

        # out arguments
        string = Gtk.MenuPositionFunc.__doc__
        self.assertEqual(string,
            "MenuPositionFunc(menu: Gtk.Menu, user_data: object) -> "
            "(x: int, y: int, push_in: bool)")

    def test_uint8_array_docstring(self):
        from gi.repository import Gio

        string = Gio.File.load_contents_finish.__doc__
        self.assertEqual(string,
            "load_contents_finish(res: Gio.AsyncResult) "
            "raises -> (bool, contents: bytes, etag_out: str)")

    def test_uint8_array_return_docstring(self):
        from gi.repository import Gtk

        string = Gtk.SelectionData.get_data.__doc__
        self.assertEqual(string, "get_data() -> bytes")

    def test_virtual_method(self):
        from gi.repository import Gtk

        string = Gtk.Widget.do_map_event.__doc__
        self.assertEqual(string, "do_map_event(event: Gdk.EventAny) -> bool")
