# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .clib.ctypesutil import gicast
from .clib.gir import GIVFuncInfoPtr
from .codegen import generate_callback


def VFuncAttribute(info):

    def func(*args, **kwargs):
        raise NotImplementedError

    func.__name__ = "do_" + info.name
    func.__doc__ = "%s(*fixme, **fixme2)" % func.__name__
    func.__module__ = info.namespace
    func._is_virtual = True
    return func
