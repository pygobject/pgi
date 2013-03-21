# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.


def VariableFactory():
    """A callable the produces unique variable names"""

    def var_factory():
        var_factory.c += 1
        return "t%d" % var_factory.c
    var_factory.c = 0

    return var_factory


class Backend(object):

    def get_library(self, namespace):
        raise NotImplementedError

    def get_function(self, lib, symbol, args, ret,
                     method=False, self_name="", throws=False):
        raise NotImplementedError

    def get_constructor(self, gtype, args):
        raise NotImplementedError

    def get_callback(self, func, args, ret):
        raise NotImplementedError

    def get_type(self, type_, may_be_null=False):
        raise NotImplementedError
