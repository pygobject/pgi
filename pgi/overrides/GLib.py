# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.overrides import get_introspection_module


GLib = get_introspection_module('GLib')

__all__ = []


def idle_add(function, **kwargs):
    priority = kwargs.get('priority', GLib.PRIORITY_DEFAULT_IDLE)
    return GLib.idle_add(priority, function)

__all__.append('idle_add')


# to support older gir
if not hasattr(GLib, "MININT8"):
    MININT8 = -2 ** 7
    MAXINT8 = 2 ** 7 - 1
    MAXUINT8 = 2 ** 8 - 1
    MININT16 = -2 ** 15
    MAXINT16 = 2 ** 15 - 1
    MAXUINT16 = 2 ** 16 - 1
    MININT32 = -2 ** 31
    MAXINT32 = 2 ** 31 - 1
    MAXUINT32 = 2 ** 32 - 1
    MININT64 = -2 ** 63
    MAXINT64 = 2 ** 63 - 1
    MAXUINT64 = 2 ** 64 - 1

    __all__.extend([
        "MININT8", "MAXINT8", "MAXUINT8", "MININT16", "MAXINT16",
        "MAXUINT16", "MININT32", "MAXINT32", "MAXUINT32",
        "MININT64", "MAXINT64", "MAXUINT64",
    ])


from pgi.gerror import PGError as GError
GError = GError
__all__.append("GError")
