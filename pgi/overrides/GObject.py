# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2013 Christoph Reiter
# Copyright (C) 2012 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# Copyright (C) 2012 Simon Feltman <sfeltman@src.gnome.org>
# Copyright (C) 2012 Bastian Winkler <buz@netbuz.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import ctypes

from pgi.overrides import get_introspection_module
from pgi.repository import GLib


GObjectModule = get_introspection_module("GObject")

GObject = GObjectModule.Object
__all__ = ["GObject"]


from pgi.gtype import PGType as GType
GType = GType
__all__.append("GType")


TYPE_INVALID = GObjectModule.type_from_name('invalid')
TYPE_NONE = GObjectModule.type_from_name('void')
TYPE_INTERFACE = GObjectModule.type_from_name('GInterface')
TYPE_CHAR = GObjectModule.type_from_name('gchar')
TYPE_UCHAR = GObjectModule.type_from_name('guchar')
TYPE_BOOLEAN = GObjectModule.type_from_name('gboolean')
TYPE_INT = GObjectModule.type_from_name('gint')
TYPE_UINT = GObjectModule.type_from_name('guint')
TYPE_LONG = GObjectModule.type_from_name('glong')
TYPE_ULONG = GObjectModule.type_from_name('gulong')
TYPE_INT64 = GObjectModule.type_from_name('gint64')
TYPE_UINT64 = GObjectModule.type_from_name('guint64')
TYPE_ENUM = GObjectModule.type_from_name('GEnum')
TYPE_FLAGS = GObjectModule.type_from_name('GFlags')
TYPE_FLOAT = GObjectModule.type_from_name('gfloat')
TYPE_DOUBLE = GObjectModule.type_from_name('gdouble')
TYPE_STRING = GObjectModule.type_from_name('gchararray')
TYPE_POINTER = GObjectModule.type_from_name('gpointer')
TYPE_BOXED = GObjectModule.type_from_name('GBoxed')
TYPE_PARAM = GObjectModule.type_from_name('GParam')
TYPE_OBJECT = GObjectModule.type_from_name('GObject')
TYPE_PYOBJECT = GObjectModule.type_from_name('PyObject')
TYPE_GTYPE = GObjectModule.type_from_name('GType')
TYPE_STRV = GObjectModule.type_from_name('GStrv')
TYPE_VARIANT = GObjectModule.type_from_name('GVariant')
TYPE_GSTRING = GObjectModule.type_from_name('GString')
TYPE_UNICHAR = TYPE_UINT
__all__ += ['TYPE_INVALID', 'TYPE_NONE', 'TYPE_INTERFACE', 'TYPE_CHAR',
            'TYPE_UCHAR', 'TYPE_BOOLEAN', 'TYPE_INT', 'TYPE_UINT', 'TYPE_LONG',
            'TYPE_ULONG', 'TYPE_INT64', 'TYPE_UINT64', 'TYPE_ENUM', 'TYPE_FLAGS',
            'TYPE_FLOAT', 'TYPE_DOUBLE', 'TYPE_STRING', 'TYPE_POINTER',
            'TYPE_BOXED', 'TYPE_PARAM', 'TYPE_OBJECT', 'TYPE_PYOBJECT',
            'TYPE_GTYPE', 'TYPE_STRV', 'TYPE_VARIANT', 'TYPE_GSTRING', 'TYPE_UNICHAR']


G_MININT8 = GLib.MININT8
G_MAXINT8 = GLib.MAXINT8
G_MAXUINT8 = GLib.MAXUINT8
G_MININT16 = GLib.MININT16
G_MAXINT16 = GLib.MAXINT16
G_MAXUINT16 = GLib.MAXUINT16
G_MININT32 = GLib.MININT32
G_MAXINT32 = GLib.MAXINT32
G_MAXUINT32 = GLib.MAXUINT32
G_MININT64 = GLib.MININT64
G_MAXINT64 = GLib.MAXINT64
G_MAXUINT64 = GLib.MAXUINT64
__all__ += ['G_MININT8', 'G_MAXINT8', 'G_MAXUINT8', 'G_MININT16',
            'G_MAXINT16', 'G_MAXUINT16', 'G_MININT32', 'G_MAXINT32',
            'G_MAXUINT32', 'G_MININT64', 'G_MAXINT64', 'G_MAXUINT64']


G_MAXDOUBLE = 1.7976931348623157e+308
G_MAXFLOAT = 3.4028234663852886e+38
G_MINDOUBLE = 2.2250738585072014e-308
G_MINFLOAT = 1.1754943508222875e-38
G_MINSHORT = - 2 ** (ctypes.sizeof(ctypes.c_short) * 8 - 1)
G_MAXSHORT = 2 ** (ctypes.sizeof(ctypes.c_short) * 8 - 1) - 1
G_MAXUSHORT = 2 ** (ctypes.sizeof(ctypes.c_short) * 8) - 1
G_MININT = - 2 ** (ctypes.sizeof(ctypes.c_int) * 8 - 1)
G_MAXINT = 2 ** (ctypes.sizeof(ctypes.c_int) * 8 - 1) - 1
G_MAXUINT = 2 ** (ctypes.sizeof(ctypes.c_uint) * 8) - 1
G_MINLONG = - 2 ** (ctypes.sizeof(ctypes.c_long) * 8 - 1)
G_MAXLONG = 2 ** (ctypes.sizeof(ctypes.c_long) * 8 - 1) - 1
G_MAXULONG = 2 ** (ctypes.sizeof(ctypes.c_ulong) * 8) - 1
G_MAXSIZE = 2 ** (ctypes.sizeof(ctypes.c_size_t) * 8) - 1
G_MINSSIZE = - 2 ** (ctypes.sizeof(ctypes.c_ssize_t) * 8 - 1)
G_MAXSSIZE = 2 ** (ctypes.sizeof(ctypes.c_ssize_t) * 8 - 1) - 1
# G_MAXOFFSET
# G_MINOFFSET

for name in ['G_MINFLOAT', 'G_MAXFLOAT', 'G_MINDOUBLE', 'G_MAXDOUBLE',
             'G_MINSHORT', 'G_MAXSHORT', 'G_MAXUSHORT', 'G_MININT', 'G_MAXINT',
             'G_MAXUINT', 'G_MINLONG', 'G_MAXLONG', 'G_MAXULONG', 'G_MAXSIZE',
             'G_MINSSIZE', 'G_MAXSSIZE', 'G_MINOFFSET', 'G_MAXOFFSET']:
    __all__.append(name)
