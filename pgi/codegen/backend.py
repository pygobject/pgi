# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.utils import CodeGenerator

class CodeGenBackend(object):

    NAME = ""

    def __init__(self):
        super(CodeGenBackend, self).__init__()

        def var_factory():
            var_factory.c += 1
            return "t%d" % var_factory.c
        var_factory.c = 0
        self._gen = CodeGenerator(var_factory)

    def var(self):
        return self._gen.var()

    def parse(self, *args, **kwargs):
        return self._gen.parse(*args, **kwargs)

    def __getattr__(self, value):
        raise NotImplementedError
