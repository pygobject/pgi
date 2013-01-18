# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest
import StringIO

from pgi.util import escape_name, unescape_name
from pgi.codegen.utils import CodeBlock


class PGIMisc(unittest.TestCase):
    def test_escape_property(self):
        self.assertEqual(escape_name("class"), "class_")
        self.assertEqual(escape_name("cla-ss"), "cla_ss")

    def test_unescape_property(self):
        self.assertEqual(unescape_name("foo_"), "foo")
        self.assertEqual(unescape_name("fo_oo_"), "fo-oo")

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
        f = StringIO.StringIO()
        a = CodeBlock()
        a.write_line("abc")
        a.pprint(f)
        self.assertEqual(f.getvalue(), "abc")
