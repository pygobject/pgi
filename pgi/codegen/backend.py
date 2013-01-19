# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.codegen.utils import parse_code


class CodeGenBackend(object):
    """Backends provide methods that produce python code. They take
    input variable nams and return a CodeBlock + output variables. If one
    method is not implemented the consumer will fall back to another backend
    if possible.

    get_library_object  - init the backend and do caching with the namespace
    get_function_object - should return something callable
    call                - code surrounding the function call (exceptions..)
    """

    NAME = "base"

    def __init__(self):
        super(CodeGenBackend, self).__init__()

        def var_factory():
            var_factory.c += 1
            return "t%d" % var_factory.c
        var_factory.c = 0

        self.var = var_factory

    def parse(self, code, **kwargs):
        return parse_code(code, self.var, **kwargs)

    def __getattr__(self, name):
        raise NotImplementedError(
            "method %r not implemented in backend %r" % (name, self.NAME))

    def get_library_object(self, namespace):
        raise NotImplementedError

    def get_function_object(self, lib, symbol, args, ret,
                            method=False, self_name="", throws=False):
        raise NotImplementedError

    def call(self, name, args):
        raise NotImplementedError
