# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from cffi import FFI

from pgi.gir import GIRepositoryPtr, GITypeTag
from pgi.codegen.backend import CodeGenBackend
from pgi.codegen.utils import CodeBlock


def typeinfo_to_cffi(info):
    tag = info.get_tag().value
    ptr = info.is_pointer()

    if not ptr:
        if tag == GITypeTag.UINT32:
            return "uint32_t"
    else:
        if tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return "char*"

    raise NotImplementedError


class CFFIBackend(CodeGenBackend):

    NAME = "cffi"

    def __init__(self, *args, **kwargs):
        super(CFFIBackend, self).__init__(*args, **kwargs)
        self._libs = {}
        try:
            self._ffi = FFI()
        except ImportError:
            raise NotImplementedError

    def get_library_object(self, namespace):
        if namespace not in self._libs:
            paths = GIRepositoryPtr().get_shared_library(namespace)
            if not paths:
                return
            path = paths.split(",")[0]
            # pfff, strip so verion
            path = path[3:].rsplit(".", 1)[0]
            self._libs[namespace] = self._ffi.dlopen(path)
        return self._libs[namespace]

    def get_function_object(self, lib, symbol, args, ret, method=False):
        if not args and not method:
            if ret:
                cffi_ret = typeinfo_to_cffi(ret.type)
                cdef = "%s %s();" % (cffi_ret, symbol)
            else:
                cdef = "void %s();" % symbol
            self._ffi.cdef(cdef)
            return CodeBlock("# " + cdef), getattr(lib, symbol)
        raise NotImplementedError

    def call(self, name, args):
        block, var = self.parse("""
# call '$name'
$ret = $name($args)
""", name=name, args=args)

        return block, var["ret"]

    def unpack_string(self, name):
        to_string = self.var()
        block, var = self.parse("""
$string = $to_string($cdata)
""", to_string=to_string, cdata=name)

        block.add_dependency(to_string, self._ffi.string)
        return block, var["string"]
