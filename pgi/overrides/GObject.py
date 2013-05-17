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

import sys
import ctypes

from pgi.overrides import get_introspection_module, override
from pgi.repository import GLib


GObjectModule = get_introspection_module("GObject")

GObject = GObjectModule.Object
__all__ = ["GObject"]


from pgi.gtype import PGType as GType
GType = GType
__all__.append("GType")


from pgi.enum import EnumBase as GEnum
GEnum = GEnum
__all__.append("GEnum")


from pgi.enum import FlagsBase as GFlags
GFlags = GFlags
__all__.append("GFlags")


from pgi.gerror import PGError as GError
GError = GError
__all__.append("GError")


from pgi.obj import InterfaceBase as GInterface
GInterface = GInterface
__all__.append("GInterface")


idle_add = GLib.idle_add
__all__.append("idle_add")


source_remove = GLib.source_remove
__all__.append("source_remove")


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


class Value(GObjectModule.Value):
    _free_on_dealloc = False

    def __new__(cls, *args, **kwargs):
        return GObjectModule.Value.__new__(cls)

    def __init__(self, value_type=None, py_value=None):
        GObjectModule.Value.__init__(self)
        if value_type is not None:
            self.init(value_type)
            if py_value is not None:
                self.set_value(py_value)

    def __del__(self):
        if self._free_on_dealloc and self.g_type != TYPE_INVALID:
            self.unset()
        GObjectModule.Value.__del__(self)

    def set_value(self, py_value):
        if self.g_type == TYPE_INVALID:
            raise TypeError("GObject.Value needs to be initialized first")
        elif self.g_type == TYPE_BOOLEAN:
            self.set_boolean(py_value)
        elif self.g_type == TYPE_CHAR:
            self.set_char(py_value)
        elif self.g_type == TYPE_UCHAR:
            self.set_uchar(py_value)
        elif self.g_type == TYPE_INT:
            self.set_int(py_value)
        elif self.g_type == TYPE_UINT:
            self.set_uint(py_value)
        elif self.g_type == TYPE_LONG:
            self.set_long(py_value)
        elif self.g_type == TYPE_ULONG:
            self.set_ulong(py_value)
        elif self.g_type == TYPE_INT64:
            self.set_int64(py_value)
        elif self.g_type == TYPE_UINT64:
            self.set_uint64(py_value)
        elif self.g_type == TYPE_FLOAT:
            self.set_float(py_value)
        elif self.g_type == TYPE_DOUBLE:
            self.set_double(py_value)
        elif self.g_type == TYPE_STRING:
            if isinstance(py_value, str):
                py_value = str(py_value)
            elif sys.version_info < (3, 0):
                if isinstance(py_value, unicode):
                    py_value = py_value.encode('UTF-8')
                else:
                    raise ValueError("Expected string or unicode but got %s%s" %
                                     (py_value, type(py_value)))
            else:
                raise ValueError("Expected string but got %s%s" %
                                 (py_value, type(py_value)))
            self.set_string(py_value)
        elif self.g_type == TYPE_PARAM:
            self.set_param(py_value)
        elif self.g_type.is_a(TYPE_ENUM):
            self.set_enum(py_value)
        elif self.g_type.is_a(TYPE_FLAGS):
            self.set_flags(py_value)
        elif self.g_type.is_a(TYPE_BOXED):
            self.set_boxed(py_value)
        elif self.g_type == TYPE_POINTER:
            self.set_pointer(py_value)
        elif self.g_type.is_a(TYPE_OBJECT):
            self.set_object(py_value)
        elif self.g_type == TYPE_UNICHAR:
            self.set_uint(int(py_value))
        # elif self.g_type == TYPE_OVERRIDE:
        #     pass
        elif self.g_type == TYPE_GTYPE:
            self.set_gtype(py_value)
        elif self.g_type == TYPE_VARIANT:
            self.set_variant(py_value)
        elif self.g_type == TYPE_PYOBJECT:
            self.set_boxed(py_value)
        else:
            raise TypeError("Unknown value type %s" % self.g_type)

    def get_value(self):
        if self.g_type == TYPE_BOOLEAN:
            return self.get_boolean()
        elif self.g_type == TYPE_CHAR:
            return self.get_char()
        elif self.g_type == TYPE_UCHAR:
            return self.get_uchar()
        elif self.g_type == TYPE_INT:
            return self.get_int()
        elif self.g_type == TYPE_UINT:
            return self.get_uint()
        elif self.g_type == TYPE_LONG:
            return self.get_long()
        elif self.g_type == TYPE_ULONG:
            return self.get_ulong()
        elif self.g_type == TYPE_INT64:
            return self.get_int64()
        elif self.g_type == TYPE_UINT64:
            return self.get_uint64()
        elif self.g_type == TYPE_FLOAT:
            return self.get_float()
        elif self.g_type == TYPE_DOUBLE:
            return self.get_double()
        elif self.g_type == TYPE_STRING:
            return self.get_string()
        elif self.g_type == TYPE_PARAM:
            return self.get_param()
        elif self.g_type.is_a(TYPE_ENUM):
            return self.get_enum()
        elif self.g_type.is_a(TYPE_FLAGS):
            return self.get_flags()
        elif self.g_type.is_a(TYPE_BOXED):
            return self.get_boxed()
        elif self.g_type == TYPE_POINTER:
            return self.get_pointer()
        elif self.g_type.is_a(TYPE_OBJECT):
            return self.get_object()
        elif self.g_type == TYPE_UNICHAR:
            return self.get_uint()
        elif self.g_type == TYPE_GTYPE:
            return self.get_gtype()
        elif self.g_type == TYPE_VARIANT:
            return self.get_variant()
        elif self.g_type == TYPE_PYOBJECT:
            pass
        else:
            return None

    def __repr__(self):
        return '<Value (%s) %s>' % (self.g_type.name, self.get_value())

Value = override(Value)
__all__.append('Value')
