# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.utils import parse_code

class CodeGenBackend(object):

    NAME = ""

    def __init__(self):
        super(CodeGenBackend, self).__init__()

        def var_factory():
            var_factory.c += 1
            return "t%d" % var_factory.c
        var_factory.c = 0

        self.var = var_factory

    def parse(self, code, **kwargs):
        return parse_code(code, self.var, **kwargs)

    def __getattr__(self, value):
        raise NotImplementedError
