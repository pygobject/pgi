# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast

from pgi.gir import GIFunctionInfoPtr
from pgi.codegen.funcgen import generate_function


def FunctionAttribute(info, namespace, name, lib):
    func_info = cast(info, GIFunctionInfoPtr)
    func = generate_function(func_info, namespace, name)
    return func
