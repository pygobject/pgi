# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import types

from enum import EnumAttribute, FlagsAttribute
from constant import ConstantAttribute
from function import FunctionAttribute
from structure import StructureAttribute
from obj import ObjectAttribute, InterfaceAttribute

import overrides
import const


_attr_list = [None, FunctionAttribute, None, StructureAttribute, None,
              EnumAttribute, FlagsAttribute, ObjectAttribute,
              InterfaceAttribute, ConstantAttribute, None, None, None, None,
              None, None, None, None, None, None]


class _ModuleAttribute(object):
    def __init__(self, info, namespace, name, lib):
        self._info = info
        self._name = name
        self._lib = lib
        self._namespace = namespace

    def __get__(self, instance, owner):
        info = self._info
        #print self._name, info.get_type(), info.get_type().value
        cls = _attr_list[info.get_type().value]
        if cls:
            name = self._name
            attr = cls(info, self._namespace, name, self._lib)
            setattr(instance or owner, name, attr)
        else:
            attr = None
        info.unref()
        return attr


class _Module(types.ModuleType):
    def __dir__(self):
        # All unresolved properties in the module class don't show up
        # using dir(module_instance), so extend it
        return list(set(dir(self.__class__) + self.__dict__.keys()))


def Module(repo, namespace, lib):
    cls = type(namespace, _Module.__bases__, dict(_Module.__dict__))

    for i in xrange(repo.get_n_infos(namespace)):
        info = repo.get_info(namespace, i)
        name = info.get_name()
        attr = _ModuleAttribute(info, namespace, name, lib)
        setattr(cls, name, attr)
        #getattr(cls, name)

    return cls(namespace)
