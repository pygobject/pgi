# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi.repository import Gtk, GLib, Gio, GObject, Atk

try:
    from gi.repository import GIMarshallingTests
    GIMarshallingTests
except ImportError:
    GIMarshallingTests = None


def skipUnlessGIMarshallingTests(func):
    return unittest.skipUnless(GIMarshallingTests,
                               "GIMarshallingTests missing")(func)

def gtk_typelib_version():
    return (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)


class TDocstring(unittest.TestCase):

    def test_doc_strings(self):
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

        self.assertTrue(
            GLib.source_remove_by_funcs_user_data.__doc__ in (
                "source_remove_by_funcs_user_data(funcs: GLib.SourceFuncs, "
                "user_data: object) -> bool",
                "source_remove_by_funcs_user_data(funcs: GLib.SourceFuncs, "
                "user_data: object or None) -> bool",
                )
            )

        self.assertEqual(
            Gtk.FileChooser.get_filenames.__doc__,
            "get_filenames() -> [str]")

        if gtk_typelib_version() < (3, 12):
            self.assertEqual(
                Gtk.init_with_args.__doc__,
                "init_with_args(argv: [str] or None, "
                "parameter_string: str or None, "
                "entries: [GLib.OptionEntry], "
                "translation_domain: str) raises "
                "-> (bool, argv: [str])")

            self.assertEqual(
                Gtk.AboutDialog.drag_begin.__doc__,
                "drag_begin(targets: Gtk.TargetList, "
                "actions: Gdk.DragAction, "
                "button: int, event: Gdk.Event) -> Gdk.DragContext")
        else:
            self.assertEqual(
                Gtk.init_with_args.__doc__,
                "init_with_args(argv: [str] or None, "
                "parameter_string: str or None, "
                "entries: [GLib.OptionEntry], "
                "translation_domain: str or None) raises "
                "-> (bool, argv: [str])")

            self.assertEqual(
                Gtk.AboutDialog.drag_begin.__doc__,
                "drag_begin(targets: Gtk.TargetList, "
                "actions: Gdk.DragAction, "
                "button: int, event: Gdk.Event or None) "
                "-> Gdk.DragContext")

        self.assertEqual(
            Gtk.AboutDialog.set_default_icon_from_file.__doc__,
            "set_default_icon_from_file(filename: str) raises -> bool")

        self.assertEqual(
            Gtk.Button.get_label.__doc__,
            "get_label() -> str")

        self.assertEqual(
            Gtk.Button.set_label.__doc__,
            "set_label(label: str) -> None")

        if hasattr(Atk.NoOpObject, "get_row_header_cells"):
            self.assertEqual(
                Atk.NoOpObject.get_row_header_cells.__doc__,
                "get_row_header_cells() -> [Atk.Object]")

        self.assertEqual(
            GLib.ByteArray.new_take.__doc__,
            "new_take(data: bytes) -> bytes")

        if hasattr(GLib.Variant, "parse_error_print_context"):
            self.assertEqual(
                GLib.Variant.parse_error_print_context.__doc__,
                "parse_error_print_context(error: GLib.Error, "
                "source_str: str) -> str")

    def test_callback_docstring(self):
        string = GLib.DestroyNotify.__doc__
        # annotations changed over time, allow both variants
        self.assertTrue(
            string in ("DestroyNotify(data: object) -> None",
                       "DestroyNotify(data: object or None) -> None"))

        # out arguments
        string = Gtk.MenuPositionFunc.__doc__
        # annotations changed over time
        possible = [
            ("MenuPositionFunc(menu: Gtk.Menu, user_data: object) -> "
             "(x: int, y: int, push_in: bool)"),
            ("MenuPositionFunc(menu: Gtk.Menu, x: int, y: int, "
             "user_data: object) -> (x: int, y: int, push_in: bool)"),
            ("MenuPositionFunc(menu: Gtk.Menu, x: int, y: int, "
             "user_data: object or None) -> (x: int, y: int, push_in: bool)"),
        ]
        self.assertTrue(string in possible)

    def test_uint8_array_docstring(self):
        string = Gio.File.load_contents_finish.__doc__
        self.assertEqual(string,
            "load_contents_finish(res: Gio.AsyncResult) "
            "raises -> (bool, contents: bytes, etag_out: str)")

    def test_uint8_array_return_docstring(self):
        string = Gtk.SelectionData.get_data.__doc__
        self.assertEqual(string, "get_data() -> bytes")

    def test_virtual_method(self):
        string = Gtk.Widget.do_map_event.__doc__
        self.assertEqual(string, "do_map_event(event: Gdk.EventAny) -> bool")

    def test_gobject_gir_method(self):
        # we want Object gir methods to show up we don't implement our self
        string = GObject.Object.run_dispose.__doc__
        self.assertEqual(string, "run_dispose() -> None")

    def test_signal(self):
        sigs = Gtk.Window.signals
        sig = sigs.set_focus
        self.assertEqual(
            sig.__doc__,
            "set_focus(window: Gtk.Window, object: Gtk.Widget) -> None")

        sigs = Gio.MountOperation.signals
        sig = Gio.MountOperation.signals.show_processes
        self.assertEqual(sig.__doc__,
            "show_processes(mount_operation: Gio.MountOperation, "
            "message: str, processes: [int], choices: [str]) -> None")

    @skipUnlessGIMarshallingTests
    def test_garray_return(self):
        func = GIMarshallingTests.garray_int_none_return
        self.assertEqual(func.__doc__, "garray_int_none_return() -> [int]")

    @skipUnlessGIMarshallingTests
    def test_glist_out(self):
        func = GIMarshallingTests.glist_utf8_container_out
        self.assertEqual(
            func.__doc__, "glist_utf8_container_out() -> list: [str]")

    @skipUnlessGIMarshallingTests
    def test_gstrv(self):
        self.assertEqual(GIMarshallingTests.gstrv_in.__doc__,
                         "gstrv_in(g_strv: [str]) -> None")
