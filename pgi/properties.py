# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast

from gitypes import GObjectClassPtr, G_TYPE_FROM_INSTANCE, GIBaseInfoPtr

from util import escape_name
from gtype import PGType


class GParamSpec(object):
    _spec = None

    def __init__(self, spec):
        self._spec = spec
        g_type = G_TYPE_FROM_INSTANCE(spec.contents.g_type_instance)
        self.__gtype__ = PGType(g_type)

    @property
    def flags(self):
        return self._spec.contents.flags.value

    @property
    def nick(self):
        return self._spec.get_nick()

    @property
    def name(self):
        return self._spec.get_name()

    @property
    def owner_type(self):
        return PGType(self._spec.contents.owner_type)

    @property
    def value_type(self):
        return PGType(self._spec.contents.value_type)

    def __repr__(self):
        return "<%s %r>" % (self.__gtype__.name, self.name)


class _GProps(object):
    def __init__(self, name):
        self.__name = name

    def __repr__(self):
        return "<GProps of %r>" % self.__name


def PropertyAttribute(info, g_type, name):
    cls = _GProps
    cls_dict = dict(cls.__dict__)

    obj_class = cast(g_type.class_peek(), GObjectClassPtr)
    for i in xrange(info.get_n_properties()):
        prop_info = info.get_property(i)
        prop_base = cast(prop_info, GIBaseInfoPtr)
        real_name = prop_base.get_name()
        spec = obj_class.find_property(real_name)
        attr_name = escape_name(real_name)
        cls_dict[attr_name] = GParamSpec(spec)
        prop_base.unref()

    return type("props", cls.__bases__, cls_dict)(name)
