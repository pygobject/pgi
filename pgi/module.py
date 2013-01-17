# Copyright 2012,2013 Christoph Reiter
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

    def __init__(self, namespace, *args, **kwargs):
        super(RepositoryWrapper, self).__init__(*args, **kwargs)
        self._namespace = namespace

    def _get_count(self, source):
        return source.get_n_infos(self._namespace)

    def _get_info(self, source, index):
        return source.get_info(self._namespace, index)

    def _get_name(self, info):
        return info.name

    def _get_by_name(self, source, name):
        return source.find_by_name(self._namespace, name)


class _Module(types.ModuleType):
    """Template class for gi modules (Gtk, ...)"""

    def __init__(self, namespace, wrapper):
        types.ModuleType.__init__(self, namespace)
        self._wrapper = wrapper

    def __dir__(self):
        names = list(self._wrapper.iternames())
        base = dir(self.__class__)
        return list(set(base + names))

    def __getattr__(self, name):
        info = self._wrapper.lookup_name(name)
        if not info:
            raise AttributeError

        cls = _attr_list[info.type.value]
        if cls:
            attr = cls(info)
            setattr(self, name, attr)
        else:
            raise AttributeError

        info.unref()
        return attr


def Module(repo, namespace):
    cls = type(namespace, _Module.__bases__, dict(_Module.__dict__))
    wrapper = RepositoryWrapper(namespace, repo)
    return cls(namespace, wrapper)
