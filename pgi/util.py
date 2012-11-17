# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import keyword
import re
from ctypes import cast, POINTER, c_void_p

from pgi import const
from pgi.gir import GITypeTag, GIInfoType
from pgi.glib import gchar_p, gpointer, gboolean, guint32, free


def typeinfo_to_ctypes(info):
    """Get a ctypes type for defining arguments and return types"""
    tag = info.get_tag().value
    ptr = info.is_pointer()

    if ptr:
        if tag == GITypeTag.UTF8:
            return gchar_p
        elif tag == GITypeTag.VOID:
            return gpointer
        elif tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
    else:
        if tag == GITypeTag.BOOLEAN:
            return gboolean
        elif tag == GITypeTag.UINT32:
            return guint32
        elif tag == GITypeTag.VOID:
            return


def set_gvalue_from_py(ptr, is_interface, tag, value):
    if is_interface:
        if tag == GIInfoType.ENUM:
            ptr.set_enum(int(value))
        else:
            return False
    else:
        if tag == GITypeTag.BOOLEAN:
            ptr.set_boolean(value)
        elif tag == GITypeTag.INT32:
            ptr.set_int(value)
        elif tag == GITypeTag.UTF8:
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            ptr.set_string(value)
        else:
            return False

    return True


def array_to_list(array):
    """Takes a null terminated array, copies the values into a list
    and frees each value and the list"""
    addrs = cast(array, POINTER(c_void_p))
    l = []
    i = 0
    value = array[i]
    while value:
        l.append(value)
        free(addrs[i])
        i += 1
        value = array[i]
    free(addrs)
    return l


def glist_to_list(g, type_):
    """Takes a glist, copies the values casted to type_ in to a list
    and frees all items and the list"""
    values = []
    item = g
    while item:
        ptr = item.contents.data
        value = cast(ptr, type_).value
        values.append(value)
        free(ptr)
        item = item.next()
    g.free()
    return values


def import_attribute(namespace, name):
    mod = __import__(const.PREFIX[-1] + "." + namespace, fromlist=[namespace])
    return getattr(mod, name)


def escape_name(text, reg=re.compile("^(%s)$" % "|".join(keyword.kwlist))):
    """Escape identifiers and keywords by changing them in a defined way
     - '-' will be replaced by '_'
     - keywords get '_' appended"""
    # see http://docs.python.org/reference/lexical_analysis.html#identifiers
    text = text.replace("-", "_")
    return reg.sub(r"\1_", text)


try:
    import pypyjit
except ImportError:
    no_jit = lambda f: f
else:
    def no_jit(f):
        def wrap(*args, **kwargs):
            try:
                if no_jit.c == 0:
                    pypyjit.set_param("off")
                no_jit.c += 1
                return f(*args, **kwargs)
            finally:
                no_jit.c -= 1
                if no_jit.c == 0:
                    pypyjit.set_param("default")
        return wrap
    no_jit.c = 0


class cached_property(object):
    """A read-only @property that is only evaluated once."""
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result
