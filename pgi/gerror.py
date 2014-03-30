# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ._compat import PY3


class PGError(RuntimeError):

    @classmethod
    def _from_gerror(cls, error):
        message = error.message
        if PY3 and message is not None:
            message = message.decode("utf-8")

        self = cls(message)
        if PY3:
            self.message = message
        self.domain = error.domain.string
        self.code = error.code
        return self


PGError.__module__ = "GLib"
PGError.__name__ = "GError"
