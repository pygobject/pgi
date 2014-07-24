# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi._compat import StringIO
from pgi.codegen.funcgen import get_type_name
from pgi.codegen.utils import VariableFactory
from pgi.codegen.utils import CodeBlock, parse_code, parse_with_objects

from pgi.repository import Gtk


class TPGICodegen(unittest.TestCase):

    def test_get_type_name(self):
        self.assertEqual(get_type_name(int), "int")
        self.assertEqual(get_type_name(str), "str")
        self.assertEqual(get_type_name(list), "list")
        self.assertEqual(get_type_name("foo"), "foo")

        self.assertEqual(get_type_name(Gtk.Window), "Gtk.Window")
        self.assertEqual(get_type_name([Gtk.Window]), "[Gtk.Window]")
        self.assertEqual(get_type_name({int: Gtk.Window}), "{int: Gtk.Window}")

        # don't change the type
        x = {int: int}
        self.assertEqual(get_type_name(x), "{int: int}")
        self.assertEqual(get_type_name(x), "{int: int}")

    def test_parse_with_objects(self):
        some_obj = object()
        some_int = 42
        block, mapping = parse_with_objects(
            "$foo=$bar", lambda *x: "X", foo=some_obj, bar=some_int)

        self.assertEqual(str(block), "X=42")
        self.assertEqual(list(block.get_dependencies().items()),
                         [("X", some_obj)])

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
        self.assertEqual(f.getvalue(), "abc\n")

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
