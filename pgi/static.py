# Copyright 2012,2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes


def _min_value(ctypes_type):
    signed = ctypes_type(-1).value == -1
    if signed:
        return - 2 ** (ctypes.sizeof(ctypes_type) * 8 - 1)
    return 0


def _max_value(ctypes_type):
    signed = ctypes_type(-1).value == -1
    return 2 ** (ctypes.sizeof(ctypes_type) * 8 - signed) - 1


G_MINDOUBLE = 2.2250738585072014e-308
G_MAXDOUBLE = 1.7976931348623157e+308
G_MINFLOAT = 1.1754943508222875e-38
G_MAXFLOAT = 3.4028234663852886e+38
G_MINSHORT = _min_value(ctypes.c_short)
G_MAXSHORT = _max_value(ctypes.c_short)
G_MAXUSHORT = _max_value(ctypes.c_ushort)
G_MININT = _min_value(ctypes.c_int)
G_MAXINT = _max_value(ctypes.c_int)
G_MAXUINT = _max_value(ctypes.c_uint)
G_MINLONG = _min_value(ctypes.c_long)
G_MAXLONG = _max_value(ctypes.c_long)
G_MAXULONG = _max_value(ctypes.c_ulong)
G_MAXSIZE = _max_value(ctypes.c_size_t)
G_MINSSIZE = _min_value(ctypes.c_ssize_t)
G_MAXSSIZE = _max_value(ctypes.c_ssize_t)
G_MINOFFSET = _min_value(ctypes.c_int64)
G_MAXOFFSET = _max_value(ctypes.c_int64)
