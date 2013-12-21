# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .clib.ctypesutil import gicast
from .clib.gir import GIFunctionInfoPtr
from .util import import_attribute
from .codegen import generate_callback


def CallbackAttribute(info):
    info = gicast(info, GIFunctionInfoPtr)

    func = generate_callback(info)
    func.__module__ = info.namespace
    func._is_callback = True

    return func
