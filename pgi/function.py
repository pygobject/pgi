# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .clib.ctypesutil import gicast
from .clib.gir import GIFunctionInfoPtr, GIFunctionInfoFlags
from .codegen.funcgen import generate_function


def FunctionAttribute(info):
    info = gicast(info, GIFunctionInfoPtr)
    throws = info.flags.value & GIFunctionInfoFlags.THROWS
    func = generate_function(info, throws=throws)
    return func
