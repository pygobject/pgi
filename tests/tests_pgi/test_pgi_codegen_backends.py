# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from pgi.codegen.cffi_backend import CFFIBackend
from pgi.codegen.ctypes_backend import CTypesBackend


class _TBackend(unittest.TestCase):

    Backend = None

    def test_misc(self):
        backend = self.Backend()
        lib = backend.get_library("GObject")
        self.assertTrue(lib)


class TBackendCFFI(_TBackend):
    Backend = CFFIBackend


class TBackendCTypes(_TBackend):
    Backend = CTypesBackend
