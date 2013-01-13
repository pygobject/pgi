# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.


class CodeGenBackend(object):

    def __init__(self, codegen):
        super(CodeGenBackend, self).__init__()
        self._gen = codegen

    def var(self):
        return self._gen.var()

    def parse(self, *args, **kwargs):
        return self._gen.parse(*args, **kwargs)

    def get_library_object(self, namespace):
        raise NotImplementedError

    def get_function_object(self, lib, symbol, args, ret):
        raise NotImplementedError
