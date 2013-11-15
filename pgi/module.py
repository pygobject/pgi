# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import types

from .enum import EnumAttribute, FlagsAttribute
from .constant import ConstantAttribute
from .function import FunctionAttribute
from .structure import StructureAttribute, UnionAttribute
from .obj import ObjectAttribute, InterfaceAttribute
from .util import InfoIterWrapper, escape_keyword, unescape_keyword


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

    __weakref__ = None

    def __init__(self, namespace, wrapper):
        types.ModuleType.__init__(self, namespace)
        self._wrapper = wrapper

    def __dir__(self):
        # get all infos and
        names = list(self._wrapper.iternames())
        names.extend(self.__dict__.keys())
        names = map(escape_keyword, names)

        # filter out not implemented ones
        implemented_names = []
        for name in list(set(names)):
            try:
                obj = getattr(self, name)
            except NotImplementedError:
                pass
            else:
                if not getattr(obj, "_is_gtype_struct", False):
                    implemented_names.append(name)

        return implemented_names

    def __getattr__(self, name):
        info = self._wrapper.lookup_name(unescape_keyword(name))
        if not info:
            raise AttributeError("%r module has not attribute %r" %
                                 (self.__class__.__name__, name))

        cls = _attr_list[info.type.value]
        if cls:
            attr = cls(info)
            setattr(self, name, attr)
        else:
            raise NotImplementedError(
                "%r attribute type not supported" % info.type)

        return attr


def Module(repo, namespace):
    cls = type(namespace, _Module.__bases__, dict(_Module.__dict__))
    wrapper = RepositoryWrapper(namespace, repo)
    return cls(namespace, wrapper)
