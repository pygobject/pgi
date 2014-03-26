# Copyright 2012-2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi import _compat
from pgi.clib import glib
from pgi.clib.glib import gboolean, gpointer, guint, guint32, GErrorPtr, gint8
from pgi.clib.glib import GSListPtr, GListPtr, gchar_p, gunichar, gdouble
from pgi.clib.glib import gfloat, guint64, gint64, gint32, guint16, gint16
from pgi.clib.glib import guint8
from pgi.clib.gobject import GType
from pgi.clib.gir import GITypeTag, GIInfoType
from pgi.clib.gobject import GCallback

from ..utils import CodeBlock


class BaseType(object):
    GI_TYPE_TAG = None
    py_type = None

    def __init__(self, gen, type_, may_be_null, may_return_null):
        self._gen = gen
        self.block = CodeBlock()
        self.type = type_
        self.may_be_null = may_be_null
        self.return_null = may_return_null

    def get_type(self, type_, may_be_null=False, may_return_null=False):
        return get_type(type_)(self._gen, type_, may_be_null, may_return_null)

    def var(self):
        return self._gen.var()

    def __getattr__(self, attr):
        if attr.endswith(("_py2", "_py3")):
            raise AttributeError(attr)
        if _compat.PY3:
            return getattr(self, attr + "_py3")
        return getattr(self, attr + "_py2")

    @classmethod
    def get_class(cls, type_):
        return cls

    def parse(self, code, **kwargs):
        block, var = self._gen.parse(code, **kwargs)
        block.write_into(self.block)
        return var

    def get_reference(self, value):
        return self.parse("""
$ptr = $ctypes.byref($value)
""", value=value)["ptr"]

    def free(self, name):
        self.parse("""
$glib.free($ptr)
""", ptr=name, glib=glib)

    def pack_pointer(self, name):
        """Returns a pointer containing the value.

        This only works for int32/uint32/utf-8..
        """

        return self.parse("""
raise $_.TypeError('Can\\'t convert %(type_name)s to pointer: %%r' %% $in_)
""" % {"type_name": type(self).__name__}, in_=name)["in_"]


_type_registry = {}


def register_type(type_tag):
    def wrap(cls):
        assert type_tag not in _type_registry
        _type_registry[type_tag] = cls
        return cls
    return wrap


def get_type(type_):
    tag_value = type_.tag.value
    if tag_value in _type_registry:
        return _type_registry[tag_value].get_class(type_)
    raise NotImplementedError("type: %r", type_.tag)


def typeinfo_to_ctypes(info, return_value=False):
    """Maps a GITypeInfo() to a ctypes type.

    The ctypes types have to be different in the case of return values
    since ctypes does 'auto unboxing' in some cases which gives
    us no chance to free memory if there is a ownership transfer.
    """

    tag = info.tag.value
    ptr = info.is_pointer

    mapping = {
        GITypeTag.BOOLEAN: gboolean,
        GITypeTag.INT8: gint8,
        GITypeTag.UINT8: guint8,
        GITypeTag.INT16: gint16,
        GITypeTag.UINT16: guint16,
        GITypeTag.INT32: gint32,
        GITypeTag.UINT32: guint32,
        GITypeTag.INT64: gint64,
        GITypeTag.UINT64: guint64,
        GITypeTag.FLOAT: gfloat,
        GITypeTag.DOUBLE: gdouble,
        GITypeTag.VOID: None,
        GITypeTag.GTYPE: GType,
        GITypeTag.UNICHAR: gunichar,
    }

    if ptr:
        if tag == GITypeTag.INTERFACE:
            return gpointer
        elif tag in (GITypeTag.UTF8, GITypeTag.FILENAME):
            if return_value:
                # ctypes does auto conversion to str and gives us no chance
                # to free the pointer if transfer=everything
                return gpointer
            else:
                return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
        elif tag == GITypeTag.ERROR:
            return GErrorPtr
        elif tag == GITypeTag.GLIST:
            return GListPtr
        elif tag == GITypeTag.GSLIST:
            return GSListPtr
        else:
            if tag in mapping:
                return ctypes.POINTER(mapping[tag])
    else:
        if tag == GITypeTag.INTERFACE:
            iface = info.get_interface()
            iface_type = iface.type.value
            if iface_type == GIInfoType.ENUM:
                return guint32
            elif iface_type == GIInfoType.OBJECT:
                return gpointer
            elif iface_type == GIInfoType.STRUCT:
                return gpointer
            elif iface_type == GIInfoType.UNION:
                return gpointer
            elif iface_type == GIInfoType.FLAGS:
                return guint
            elif iface_type == GIInfoType.CALLBACK:
                return GCallback

            raise NotImplementedError(
                "Could not convert interface: %r to ctypes type" % iface.type)
        else:
            if tag in mapping:
                return mapping[tag]

    raise NotImplementedError("Could not convert %r to ctypes type" % info.tag)
