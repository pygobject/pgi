# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import keyword
import re
from ctypes import cast, POINTER, c_void_p

from pgi import const
from pgi.gir import GITypeTag, GIInfoType
from pgi.glib import free
from pgi.gobject import GValuePtr, GValue


class Super(object):
    """Biggest hack ever?"""

    def __init__(self, name):
        self.__name = name
        self.__instances = {}

    def __get__(self, instance, owner):
        cls = self.__instances.setdefault(instance, owner)
        next_cls = cls.__mro__[1]
        if next_cls is not object:
            func = getattr(next_cls, self.__name)
            self.__instances[instance] = next_cls
            return lambda *args, **kwargs: func(instance, *args, **kwargs)
        del self.__instances[instance]
        return lambda *args, **kwargs: True


class InfoIterWrapper(object):
    """Allow fast name lookup for gi structs.

    Most GIBaseInfo struct define an interface to iterate sub structs.
    Those are usually sorted by name, so we can do a binary search.
    Since they aren't guaranteed to be sorted we have to look through all
    of them in case of a miss.

    Slow/fast paths are separated since we need to check all fast paths
    of multiple sources before falling back to the slow ones.
    """

    def __init__(self, source):
        super(InfoIterWrapper, self).__init__()
        self._source = source
        self.__infos = {}
        self.__names = {}
        self.__count = -1

    def _get_count(self, source):
        raise NotImplementedError

    def _get_info(self, source, index):
        raise NotImplementedError

    def _get_name(self, info):
        raise NotImplementedError

    def _get_by_name(self, source, name):
        raise NotImplementedError

    def __get_name_cached(self, index):
        info = self.__get_info_cached(index)
        name = self._get_name(info)
        self.__names[name] = info
        return name

    def __get_info_cached(self, index):
        if index not in self.__infos:
            self.__infos[index] = self._get_info(self._source, index)
        return self.__infos[index]

    def __get_count_cached(self):
        if self.__count == -1:
            self.__count = self._get_count(self._source)
        return self.__count

    def lookup_name_fast(self, name):
        """Might return a struct"""

        if name in self.__names:
            return self.__names[name]

        count = self.__get_count_cached()
        lo = 0
        hi = count
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__get_name_cached(mid) < name:
                lo = mid + 1
            else:
                hi = mid

        if lo != count and self.__get_name_cached(lo) == name:
            return self.__get_info_cached(lo)

    def lookup_name_slow(self, name):
        """Returns a struct if one exists"""

        for index in xrange(self.__get_count_cached()):
            if self.__get_name_cached(index) == name:
                return self.__get_info_cached(index)

    def lookup_name(self, name):
        """Returns a struct if one exists"""

        try:
            info = self._get_by_name(self._source, name)
        except NotImplementedError:
            pass
        else:
            if info:
                return info
            return

        info = self.lookup_name_fast(name)
        if info:
            return info
        return self.lookup_name_slow(name)

    def iternames(self):
        """Iterate over all struct names in no defined order"""

        for index in xrange(self.__get_count_cached()):
            yield self.__get_name_cached(index)

    def clear(self):
        """Unref all structs and clear cache"""

        self.__infos.clear()
        self.__names.clear()


def gparamspec_to_gvalue_ptr(spec, value):
    type_ = spec._info.get_type()
    tag = type_.tag.value

    ptr = GValuePtr(GValue())
    ptr.init(spec.value_type._type.value)

    is_interface = False
    if tag == GITypeTag.INTERFACE:
        iface_info = type_.get_interface()
        tag = iface_info.type.value
        is_interface = True

    if not set_gvalue_from_py(ptr, is_interface, tag, value):
        ptr.unset()
        return None

    return ptr


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
        elif tag == GITypeTag.UINT32:
            ptr.set_uint(value)
        elif tag == GITypeTag.DOUBLE:
            ptr.set_double(value)
        elif tag == GITypeTag.FLOAT:
            ptr.set_float(value)
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
    mod = __import__(const.PREFIX[-1] + "." + namespace, fromlist=[name])
    return getattr(mod, name)


def import_module(namespace):
    mod = __import__(const.PREFIX[-1], fromlist=[namespace])
    return getattr(mod, namespace)


def escape_builtin(text):
    """Escape a name so it doesn't shadow a builtin"""
    import __builtin__
    while text in dir(__builtin__):
        text = text + "_"
    return text


def escape_name(text, reg=re.compile("^(%s)$" % "|".join(keyword.kwlist))):
    """Escape identifiers and keywords by changing them in a defined way
     - '-' will be replaced by '_'
     - keywords get '_' appended"""
    # see http://docs.python.org/reference/lexical_analysis.html#identifiers
    text = text.replace("-", "_")
    return reg.sub(r"\1_", text)


def unescape_name(text):
    return text.rstrip("_").replace("_", "-")

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

    def __set__(self, instance, value):
        raise AttributeError
