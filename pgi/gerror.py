# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.


class PGError(RuntimeError):

    def __init__(self, error):
        self.domain = error.domain.string
        self.code = error.code
        self.message = error.message

PGError.__module__ = "GLib"
PGError.__name__ = "GError"
