# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes
import unittest
import contextlib

from pgi.codegen.cffi_backend import CFFIBackend
from pgi.codegen.ctypes_backend import CTypesBackend
from pgi.codegen.null_backend import NullBackend
from pgi.clib.gir import GITypeTag



class FakeTypeInfo(object):
    def __init__(self, tag):
        self._tag = tag

    @property
    def tag(self):
        return ctypes.c_uint(self._tag)


@contextlib.contextmanager
def executor(backend, type_):
    """Compiles and executes the generated code on demand and takes and
    returns real values::

        with executor(backend, GITypeTag.INT32) as var:
            self.assertEqual(var.pack_in(4), 4)
            self.assertEqual(var.unpack_out(var.pack_out(42)), 42)

    """

    class Compiler(object):
        def __init__(self, backend, var, key):
            self.backend = backend
            self.var = var
            self.key = key

        def __call__(self, *args):
            arg_names = [self.backend.var() for arg in args]
            out_names = getattr(self.var, self.key)(*arg_names)
            if not isinstance(out_names, (list, tuple)):
                out_names = [out_names]

            block, var = backend.parse("""
def func($args):
    $body
    return $out
""", args=", ".join(arg_names), body=self.var.block, out=", ".join(out_names))

            self.var.block.clear()
            return block.compile()["func"](*args)

    class VarWrapper(object):

        def __init__(self, backend, var):
            self.backend = backend
            self.var = var

        def __getattr__(self, key):
            return Compiler(self.backend, self.var, key)

    yield VarWrapper(backend, backend.get_type(FakeTypeInfo(type_)))



class _TBackend(unittest.TestCase):

    Backend = None

    def setUp(self):
        self.backend = self.Backend()

    def test_misc(self):
        lib = self.backend.get_library("GObject")
        self.assertTrue(lib)

    def test_basic_int(self):
        for type_tag in [GITypeTag.INT16, GITypeTag.UINT16, GITypeTag.INT32,
                         GITypeTag.UINT32, GITypeTag.INT64, GITypeTag.UINT64]:
            with executor(self.backend, type_tag) as var:
                self.assertEqual(var.pack_in(42), 42)
                self.assertEqual(var.unpack_return(42), 42)
                self.assertEqual(var.unpack_out(var.new()), 0)
                self.assertEqual(var.unpack_out(var.pack_out(42)), 42)


class TBackendCFFI(_TBackend):
    Backend = CFFIBackend


class TBackendCTypes(_TBackend):
    Backend = CTypesBackend


class TNullBackend(unittest.TestCase):

    def test_same_varfac(self):
        # make sure everything uses the same variable factory
        backend = NullBackend()
        b1, v = backend.parse("$foo", foo=object())
        b2, v = backend.parse("$foo", foo=object())
        b2.write_into(b1)
