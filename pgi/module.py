# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import types

from pgi.enum import EnumAttribute, FlagsAttribute
from pgi.constant import ConstantAttribute
from pgi.function import FunctionAttribute
from pgi.structure import StructureAttribute
from pgi.obj import ObjectAttribute, InterfaceAttribute
from pgi.union import UnionAttribute
from pgi.util import InfoIterWrapper


_attr_list = [None, FunctionAttribute, None, StructureAttribute, None,
              EnumAttribute, FlagsAttribute, ObjectAttribute,
              InterfaceAttribute, ConstantAttribute, None, UnionAttribute,
              None, None, None, None, None, None, None, None]


class RepositoryWrapper(InfoIterWrapper):
    def _get_count(self, source):
        return source.get_n_infos(self._namespace)

    def _get_info(self, source, index):
        return source.get_info(self._namespace, index)

    def _get_name(self, info):
        return info.get_name()


class _Module(types.ModuleType):
    """Template class for gi modules (Gtk, ...)"""

    def __init__(self, namespace, wrapper, lib):
        types.ModuleType.__init__(self, namespace)
        self._wrapper = wrapper
        self._namespace = namespace
        self._lib = lib

    def __dir__(self):
        names = list(self._wrapper.iternames())
        base = dir(self.__class__)
        return list(set(base + names))

    def __getattr__(self, name):
        # XXX: This is the only invalid access (why?) on import which forces
        # us to search all infos.. ignore it for now
        if self._namespace == "GObject" and name == "GObject":
            raise AttributeError

        info = self._wrapper.lookup_name(name)
        if not info:
            raise AttributeError

        cls = _attr_list[info.get_type().value]
        if cls:
            attr = cls(info, self._namespace, name, self._lib)
            setattr(self, name, attr)
        else:
            raise AttributeError

        info.unref()
        return attr


def Module(repo, namespace, lib):
    cls = type(namespace, _Module.__bases__, dict(_Module.__dict__))
    wrapper = RepositoryWrapper(repo, namespace)
    return cls(namespace, wrapper, lib)
