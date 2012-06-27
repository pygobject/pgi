# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import keyword
import re
from ctypes import cast

import const


def glist_get_all(g, type_):
    values = []
    while g:
        value = cast(g.contents.data, type_).value
        values.append(value)
        g = g.next()
    return values


def import_attribute(namespace, name):
    mod = __import__(const.PREFIX + "." + namespace, fromlist=[namespace])
    return getattr(mod, name)


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


def escape_name(text, reg=re.compile("^(%s)$" % "|".join(keyword.kwlist))):
    """Escape identifiers and keywords by changing them in a defined way
     - '-' will be replaced by '_'
     - keywords get '_' appended"""
    # see http://docs.python.org/reference/lexical_analysis.html#identifiers
    text = text.replace("-", "_")
    return reg.sub(r"\1_", text)
