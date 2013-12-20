# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .clib.ctypesutil import gicast
from .clib.gir import GIFunctionInfoPtr


def CallbackAttribute(info):
    info = gicast(info, GIFunctionInfoPtr)

    cls = type(info.name, (object,), dict())
    cls.__module__ = info.namespace

    return cls
