# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi.codegen.funcgen import get_type_name
from pgi.codegen.utils import VariableFactory


class TPGICodegen(unittest.TestCase):

    def test_get_type_name(self):
        self.assertEqual(get_type_name(int), "int")
        self.assertEqual(get_type_name(str), "str")
        self.assertEqual(get_type_name(list), "list")
        self.assertEqual(get_type_name("foo"), "foo")

        from pgi.repository import Gtk

        self.assertEqual(get_type_name(Gtk.Window), "Gtk.Window")
        self.assertEqual(get_type_name([Gtk.Window]), "[Gtk.Window]")
        self.assertEqual(get_type_name({int: Gtk.Window}), "{int: Gtk.Window}")

        # don't change the type
        x = {int: int}
        self.assertEqual(get_type_name(x), "{int: int}")
        self.assertEqual(get_type_name(x), "{int: int}")


class TVariableFactory(unittest.TestCase):

    def test_basic(self):
        var = VariableFactory()
        self.assertNotEqual(var(), var())

    def test_blacklist(self):
        default_first = VariableFactory()()
        var = VariableFactory([default_first])()
        self.assertNotEqual(var, default_first)

        var = VariableFactory(["foobar"])
        self.assertNotEqual(var.request_name("foobar"), "foobar")

    def test_cache(self):
        obj = object()
        var = VariableFactory()
        self.assertEqual(var(obj), var(obj))
        self.assertNotEqual(var(obj), var())

    def test_request(self):
        var = VariableFactory()
        first = var()
        self.assertNotEqual(var.request_name(first), first)
        self.assertEqual(var.request_name("foobar"), "foobar")
