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


_attr_list = [None, FunctionAttribute, None, StructureAttribute, None,
              EnumAttribute, FlagsAttribute, ObjectAttribute,
              InterfaceAttribute, ConstantAttribute, None, UnionAttribute,
              None, None, None, None, None, None, None, None]


class RepositoryWrapper(object):
    """Allows iteration over all infos and fast access by name.

    Infos are usually sorted by name but I'm not sure that's guaranteed,
    so try and fall back to search all infos.
    """

    def __init__(self, repository, namespace):
        super(RepositoryWrapper, self).__init__()
        self._count = repository.get_n_infos(namespace)
        self._namespace = namespace
        self._repository = repository
        self._infos = [None] * self._count
        self._name = {}

    def __len__(self):
        return self._count

    def iternames(self):
        for index in xrange(self._count):
            yield self._get_name(index)

    def _get_name(self, index):
        pair = self._infos[index]
        if not pair:
            info = self._repository.get_info(self._namespace, index)
            name = info.get_name()
            self._name[name] = info
            pair = (name, info)
            self._infos[index] = pair
        return pair[0]

    def get_for_name(self, name):
        if name in self._name:
            return self._name[name]

        lo = 0
        hi = self._count
        while lo < hi:
            mid = (lo + hi) // 2
            if self._get_name(mid) < name:
                lo = mid + 1
            else:
                hi = mid

        if lo != self._count and self._get_name(lo) == name:
            return self._infos[lo][1]

        # fallback
        for index in xrange(self._count):
            if self._get_name(index) == name:
                return self._infos[index][1]

        raise KeyError


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

        try:
            info = self._wrapper.get_for_name(name)
        except KeyError:
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
