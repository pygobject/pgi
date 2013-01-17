# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import byref

from pgi.gir import GIRepository
from pgi.gobject import GType, GTypeFlags, GTypeFundamentalFlags
from pgi.glib import guint, free
from pgi.util import import_attribute, cached_property


class PGType(object):
    __types = {}

    def __new__(cls, type_):
        value = type_.value
        if value in cls.__types:
            return cls.__types[value]
        obj = super(PGType, cls).__new__(cls)
        cls.__types[value] = obj
        return obj

    def __init__(self, type_):
        self._type = type_

    def __get_gtype_list(self, function):
        length = guint()
        array = getattr(self._type, function)(byref(length))
        # copy the gtypes and free the array so we don't leak
        items = [PGType(GType(v.value)) for v in array[:length.value]]
        free(array)
        return items

    @cached_property
    def children(self):
        return self.__get_gtype_list("children")

    @cached_property
    def interfaces(self):
        return self.__get_gtype_list("interfaces")

    @classmethod
    def from_name(self, name):
        type_ = GType.from_name(name)
        if type_.value == 0:
            raise RuntimeError("unknown type name")
        return PGType(type_)

    @cached_property
    def fundamental(self):
        return PGType(self._type.fundamental)

    def has_value_table(self):
        return bool(self._type.value_table_peek)

    def is_a(self, type_):
        return self._type.is_a(type_._type)

    def is_abstract(self):
        return self._type.test_flags(GTypeFlags.ABSTRACT)

    def is_classed(self):
        return self._type.test_flags(GTypeFundamentalFlags.CLASSED)

    def is_deep_derivable(self):
        return self._type.test_flags(GTypeFundamentalFlags.DEEP_DERIVABLE)

    def is_derivable(self):
        return self._type.test_flags(GTypeFundamentalFlags.DERIVABLE)

    def is_instantiatable(self):
        return self._type.test_flags(GTypeFundamentalFlags.INSTANTIATABLE)

    def is_interface(self):
        return self.fundamental._type.value == (2 << 2)

    def is_value_abstract(self):
        return self._type.test_flags(GTypeFlags.VALUE_ABSTRACT)

    def is_value_type(self):
        return self._type.check_is_value_type

    @cached_property
    def parent(self):
        return PGType(self._type.parent)

    @cached_property
    def name(self):
        return self._type.name or "invalid"

    @cached_property
    def depth(self):
        return self._type.depth

    @cached_property
    def pytype(self):
        if self._type.value == 0:
            return None

        repo = GIRepository.get_default()
        base_info = repo.find_by_gtype(self._type)
        if not base_info:
            return None
        name = base_info.name
        namespace = base_info.namespace
        base_info.unref()

        return import_attribute(namespace, name)

    def __eq__(self, other):
        return self._type.value == other._type.value

    def __neq__(self, other):
        return not self == other

    def __repr__(self):
        return "<GType %s (%d)>" % (self.name, self._type.value)
